from django.urls import path
from .views import IssueBookAPIView, IssueBookDetailAPIView, ReturnBookAPIView, RenewBookAPIView


urlpatterns = [
    path('', IssueBookAPIView.as_view()),
    path('<int:pk>/', IssueBookDetailAPIView.as_view()),
    path('<int:pk>/return/', ReturnBookAPIView.as_view()),
    path('<int:pk>/renew/', RenewBookAPIView.as_view()),
]