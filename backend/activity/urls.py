from django.urls import path
from .views import RecentActivityAPIView

urlpatterns = [
    path(
        "recent-activities/",
        RecentActivityAPIView.as_view(),
        name="recent-activities",
    ),
]