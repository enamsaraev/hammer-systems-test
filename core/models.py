from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fileds):
        """Creates and saves a new user"""

        if not phone:
            raise ValueError('User must have a phone number')

        user = self.model(phone=phone, **extra_fileds)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password):
        """Creates and saves a new superuser"""

        user = self.create_user(phone, password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user
    

class ActiveUserManager(models.Manager):
    "Create a user relation by invite code ativating if its not exists"

    def create(self, **obj_data) -> Any:
        if not ActiveUser.objects.filter(user=obj_data['user'], user_profile=obj_data['user_profile']):
            return super().create(**obj_data)


class User(AbstractBaseUser, PermissionsMixin):
    """Custon user model that supports using phone number instead of username"""

    phone = models.CharField(max_length=30, 
                             unique=True,
                             verbose_name=_('Телефон пользователя'),)
    invite_code = models.CharField(max_length=6,
                                   null=False, 
                                   blank=False,
                                   verbose_name=_('Invite code пользователя'),)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    deleted = models.BooleanField(default=True,
                                  verbose_name=_('Удалить'),
                                  help_text=_('Выбрать, если нужно удалить пользователя'),)

    first_name = None
    last_name = None
    username = None

    USERNAME_FIELD = 'phone'

    objects = UserManager()
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.phone


class UserProfile(models.Model):
    "Custom user profile model"

    user = models.OneToOneField('User',
                                on_delete=models.CASCADE,
                                related_name='userprofile')
    username = models.CharField(max_length=255,
                                null=True,
                                blank=True,
                                verbose_name=_('Имя'),)
    email = models.EmailField(max_length=255,
                              blank=True,
                              null=True,
                              verbose_name=_('Почта'),)
    activate_code = models.BooleanField()
    active_user = models.OneToOneField('User',
                                       on_delete=models.SET_NULL,
                                       null=True,
                                       blank=True,
                                       related_name='active_user_userprofile')

    def set_activate_code(self):
        "Switch activate_code on true if user use invite code"
        self.activate_code = True
        self.save(update_fields=['activate_code'])

    def set_active_user(self, user_profile):
        "Add a relation to user which code was activated"
        self.active_user = user_profile.user
        self.save(update_fields=['active_user'])

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self) -> str:
        return self.user.phone
        
class ActiveUser(models.Model):
    """
        Contains a relation abour users who set invite code
        user: from
        user_profile: to another user profile whos code was entered
    """
    user = models.ForeignKey('User',
                             on_delete=models.CASCADE,
                             related_name='user_activeusers')
    user_profile = models.ForeignKey('UserProfile',
                                     on_delete=models.CASCADE,
                                     related_name='activeusers')
    

    objects = ActiveUserManager()

    class Meta:
        verbose_name = 'Связи по активации кода приглашения'
        verbose_name_plural = 'Связи по активации кода приглашения'

    def __str__(self) -> str:
        return f'{self.user.phone} -> {self.user_profile.user.phone}'
    