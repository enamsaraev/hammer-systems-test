import string
import random

from dataclasses import dataclass
from typing import Any

from core.models import User, UserProfile, ActiveUser

from user_management.tasks import send_code


@dataclass
class LoginCodeCreation:
    code = ''

    def __call__(self, *args: Any, **kwds: Any) -> str:
        self._generate_login_code()
        return self.code

    def _generate_login_code(self) -> None:
        digits = string.digits
        self.code = ''.join(random.sample(digits, 4))


@dataclass
class FindUser:
    user_id: int = None
    code: str = ''
    phone: str = ''

    def __call__(self, *args: Any, **kwds: Any) -> User or None:
        if self.phone:
            return User.objects.filter(phone=self.phone).last()
        elif self.code:
            return User.objects.filter(code=self.code).last()
        elif self.user_id:
            return User.objects.filter(id=self.user_id).last()
    

@dataclass
class UserCreationHelper:
    phone: str
    login_code: str

    def __call__(self, *args: Any, **kwds: Any) -> None:
        return self._create_new_user()

    def _create_new_user(self):
        invite_code = self._generate_invite_code()

        user = User.objects.create(phone=self.phone,
                            invite_code=invite_code,
                            password=self.login_code)
        
        return user

    def _generate_invite_code(self) -> str:
        letters_and_digits = string.ascii_uppercase + string.digits
        rand_invite_code = ''.join(random.sample(letters_and_digits, 6))
        
        return rand_invite_code
    

@dataclass
class FindUserProfile:
    user_id: int = None
    code: str = ''

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self._find_user_profile()

    def _find_user_profile(self) -> UserProfile or None:
        if self.user_id:
            return UserProfile.objects.filter(user__id=self.user_id).prefetch_related('activeusers').last()
        elif self.code:
            return UserProfile.objects.filter(user__invite_code=self.code).last()


def send_login_code(code, user) -> None:
    user.set_password(code)
    user.save()

    send_code.delay(code=code)


class InviteCodeHelper:
    def __init__(self, user_id, code) -> None:
        self.user_id = user_id
        self.code = code
        self.from_user_profile = None

    def make_decision(self) -> UserProfile or str:
        self._check_code_invitation_exists()
        if isinstance(self.from_user_profile, UserProfile) and not self.from_user_profile.activate_code:
            return self._create_invitation()
        
        return 'You are trying to add another code or user data is not exists'

    def _check_code_invitation_exists(self) -> None:
        self.from_user_profile = FindUserProfile(user_id=self.user_id)()
    
    def _get_invitation_data(self) -> User and UserProfile:
        user = FindUser(user_id=self.user_id)()
        to_user_profile = FindUserProfile(code=self.code)()

        return user, to_user_profile

    def _create_invitation(self) -> UserProfile or str:  
        user, user_profile = self._get_invitation_data()

        if user and user_profile:
            ActiveUser.objects.create(user=user, user_profile=user_profile)
            self.from_user_profile.set_activate_code()

            return user_profile

    