from django.contrib import admin
from django.urls import path
from .views import UserAPIView, UserDetailAPIView,CreatePasswordAPIView, LoginAPIView, AdminDashboardAPIView, LibrarianAPIView, NormalUserAPIView,LibrarianDashboardAPIView, UserDashboardAPIView, ReportsAPIView

urlpatterns = [
    path('login/',LoginAPIView.as_view()),
    path('users/', UserAPIView.as_view()),
    path('users/<int:pk>/', UserDetailAPIView.as_view()),
    path('create-password/<uuid:token>/', CreatePasswordAPIView.as_view()),
    path('admin/dashboard/',AdminDashboardAPIView.as_view()),
    path('librarians/', LibrarianAPIView.as_view()),
    path('normal-users/',NormalUserAPIView.as_view()),
    path('librarian/dashboard/',LibrarianDashboardAPIView.as_view()),
    path('user/dashboard/',UserDashboardAPIView.as_view()),
    path('reports/', ReportsAPIView.as_view())
]
