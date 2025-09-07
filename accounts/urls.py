from django.urls import path
from .views import (
    SignupView,
    LoginView,
    InviteMemberView,
    MyMembershipsView,
    SwitchOrganizationView,
    ResetPasswordConfirmView,
    CurrentUserView
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("me/", CurrentUserView.as_view(), name="current-user"),
    path("organizations/invite/", InviteMemberView.as_view(), name="invite-member"),
    path("reset-password/<uidb64>/<token>/", ResetPasswordConfirmView.as_view(), name="reset-password-confirm"),
    path("me/memberships/", MyMembershipsView.as_view(), name="my-memberships"),
    path("switch-org/", SwitchOrganizationView.as_view(), name="switch-org"),
]
