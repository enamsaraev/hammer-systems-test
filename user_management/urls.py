from django.urls import path, include

from user_management.views import UserLogin, UserConfirmation, UserProfile, ActivateCode


urlpatterns = [
    path('login/', UserLogin.as_view()),
    path('confirm/', UserConfirmation.as_view()),
    path('user-profile/', UserProfile.as_view()),
    path('user-profile/activate-code/', ActivateCode.as_view()),
]