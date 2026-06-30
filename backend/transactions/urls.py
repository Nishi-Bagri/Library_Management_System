from django.urls import path
from .views import IssueBookAPIView, MyBooksAPIView, IssueBookDetailAPIView, ReturnBookAPIView, RenewBookAPIView,UserSummaryAPIView, FineHistoryAPIView,FineSummaryAPIView


urlpatterns = [
    path('', IssueBookAPIView.as_view()),
    path('my-books/', MyBooksAPIView.as_view()),
    path('<int:pk>/', IssueBookDetailAPIView.as_view()),
    path('<int:pk>/return/', ReturnBookAPIView.as_view()),
    path('<int:pk>/renew/', RenewBookAPIView.as_view()),
    path("user-summary/<int:user_id>/", UserSummaryAPIView.as_view()),
    path("reports/fine-summary/",FineSummaryAPIView.as_view(),),
    path("reports/fine-history/<int:user_id>/",FineHistoryAPIView.as_view(),),
]