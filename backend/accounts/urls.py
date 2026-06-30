from django.contrib import admin
from django.urls import path
from .views import (
    UserAPIView,
    UserDetailAPIView,
    CreatePasswordAPIView,
    LoginAPIView,
    AdminDashboardAPIView,
    LibrarianAPIView,
    NormalUserAPIView,
    LibrarianDashboardAPIView,
    UserDashboardAPIView,
    ReportsAPIView,
    ForgotPasswordAPIView,
    PasswordResetRequestListAPIView,
    ApprovePasswordResetAPIView,
    RejectPasswordResetAPIView,
    ResetPasswordAPIView,
    DeactivationRequestListAPIView,
    AccountDeactivationRequestAPIView,
    RejectDeactivationAPIView,
    MyProfileAPIView,
    ChangePasswordAPIView
)
urlpatterns = [
    path('login/',LoginAPIView.as_view()),
    path('users/', UserAPIView.as_view()),
    path('users/<int:pk>/', UserDetailAPIView.as_view()),
    path('create-password/<uuid:token>/', CreatePasswordAPIView.as_view()),
    path('reset-password/<uuid:token>/',ResetPasswordAPIView.as_view()),
    path('admin/dashboard/',AdminDashboardAPIView.as_view()),
    path('librarians/', LibrarianAPIView.as_view()),
    path('normal-users/',NormalUserAPIView.as_view()),
    path('librarian/dashboard/',LibrarianDashboardAPIView.as_view()),
    path('user/dashboard/',UserDashboardAPIView.as_view()),
    path('reports/', ReportsAPIView.as_view()),
    
    path("profile/",MyProfileAPIView.as_view(),name="my-profile",),
    
    path( "forgot-password/", ForgotPasswordAPIView.as_view()),
    
    path("password-reset-requests/",PasswordResetRequestListAPIView.as_view()),

    path("password-reset-requests/<int:pk>/approve/",ApprovePasswordResetAPIView.as_view()),

    path("password-reset-requests/<int:pk>/reject/",RejectPasswordResetAPIView.as_view()),
    
    path("deactivation-requests/",DeactivationRequestListAPIView.as_view()),

    path("deactivation-request/",AccountDeactivationRequestAPIView.as_view()),
    
    path("deactivation-request/<int:pk>/reject/",RejectDeactivationAPIView.as_view()),

    path("change-password/", ChangePasswordAPIView.as_view(),name="change-password",)
]
