from django.urls import path
from .views import (
    SignupView,
    LoginView,
    InviteMemberView,
    MyMembershipsView,
    SwitchOrganizationView,
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("organizations/<int:org_id>/invite/", InviteMemberView.as_view(), name="invite-member"),
    path("me/memberships/", MyMembershipsView.as_view(), name="my-memberships"),
    path("switch-org/", SwitchOrganizationView.as_view(), name="switch-org"),
]
