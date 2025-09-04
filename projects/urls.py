from django.urls import path
from .views import ProjectCreateView

urlpatterns = [
    path("organizations/<int:org_id>/projects/", ProjectCreateView.as_view(), name="create-project"),
]
