from django.urls import path, include

from user_management.views import UserLogin, UserConfirmation, UserProfile, ActivateCode

app_name = 'user'


urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('confirm/', UserConfirmation.as_view(), name='confirm'),
    path('user-profile/', UserProfile.as_view(), name='profile'),
    path('user-profile/activate-code/', ActivateCode.as_view(), name='code'),
]