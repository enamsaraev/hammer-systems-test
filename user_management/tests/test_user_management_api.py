import pytest

from rest_framework.test import APIClient
from django.urls import reverse
from mixer.backend.django import mixer

from core.models import User, UserProfile, ActiveUser

api = APIClient()


def test_login_with_exising_user(db, api):
    user = mixer.blend('core.User', phone='88000000000')

    request_data_login = {
        "phone": user.phone
    }
    request = api.post(reverse('user:login'), data=request_data_login)

    assert request.status_code == 200
    assert 'code' in request.data

    user.set_password(request.data['code'])
    user.save()

    request_data_confirm = {
        "phone": user.phone,
        "code": request.data['code']
    }
    request = api.post(reverse('user:confirm'), data=request_data_confirm)

    assert request.data['login'] == True


def test_login_with_a_new_user(db, api):
    phone = '88000000000'
    request_data_login = {
        "phone": phone
    }
    request = api.post(reverse('user:login'), data=request_data_login)
    new_user = User.objects.last()

    assert request.status_code == 201
    assert 'code' in request.data
    assert new_user.phone == phone

    new_user.set_password(request.data['code'])
    new_user.save()

    request_data_confirm = {
        "phone": new_user.phone,
        "code": request.data['code']
    }
    request = api.post(reverse('user:confirm'), data=request_data_confirm)

    assert request.data['login'] == True


def test_acitvate_invite_code(db, api_login):
    api_login, _ = api_login

    from_user = mixer.blend('core.User')
    to_user = mixer.blend('core.User')
    profile_from_user = mixer.blend('core.UserProfile', user=from_user, activate_code=False, active_user=None)
    profile_to_user = mixer.blend('core.UserProfile', user=to_user, activate_code=False, active_user=None)

    request_data = {
        "user_id": from_user.id,
        "code": to_user.invite_code
    }
    request = api_login.post(reverse('user:code'), data=request_data)
    assert request.status_code == 200

    profile_from_user_updated = UserProfile.objects.get(user=profile_from_user.user)
    assert profile_from_user_updated.activate_code == True
    assert profile_from_user_updated.active_user == to_user

    assert request.data['activated_profile']['activeusers'][0]['phone']== from_user.phone

    active_user_realition = ActiveUser.objects.last()
    assert active_user_realition.user == from_user
    assert active_user_realition.user_profile == profile_to_user


def test_check_user_cant_activate_invite_code(db, api_login):
    api_login, _ = api_login

    active_user = mixer.blend('core.User')

    from_user = mixer.blend('core.User')
    to_user = mixer.blend('core.User')
    mixer.blend('core.UserProfile', user=from_user, activate_code=True, active_user=active_user)
    mixer.blend('core.UserProfile', user=to_user, activate_code=False, active_user=None)

    request_data = {
        "user_id": from_user.id,
        "code": to_user.invite_code
    }
    request = api_login.post(reverse('user:code'), data=request_data)
    assert request.status_code == 400