from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from transactions.models import IssueBook

from activity.utils import log_activity

from django.contrib.auth.hashers import make_password

from datetime import timedelta
from django.utils import timezone
from uuid import uuid4
from .pagination import UserPagination

from books.models import Book
from transactions.models import IssueBook
from django.db.models import Sum

from .models import User, PasswordHistory, PasswordResetRequest,AccountDeactivationRequest
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    CreatePasswordSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
    PasswordResetRequestSerializer,
    AccountDeactivationRequestSerializer,
    ChangePasswordSerializer,
)

class MyProfileAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(serializer.data)

class ChangePasswordAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ChangePasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = request.user

        current_password = serializer.validated_data["current_password"]
        new_password = serializer.validated_data["new_password"]

        if not user.check_password(current_password):
            return Response(
                {
                    "error": "Current password is incorrect. "
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if current_password == new_password:
            return Response(
                {"error": "current password is incorrect. "},
                status= status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()

        PasswordHistory.objects.create(
            user = user,
            changed_by = user,
            reason = "PASSWORD_CHANGED"
        )

        return Response(
            {
                "message": "Password changed successfully. "
            },
            status=status.HTTP_200_OK
        )

class UserAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        users = User.objects.all().order_by("id")

        paginator = UserPagination()

        paginated_users = paginator.paginate_queryset(users, request)

        serializer = UserSerializer(
            paginated_users,
            many=True
        )
        
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):

        creator = request.user

        role = request.data.get('role')

        if creator.role == 'ADMIN':

            if role not in ['LIBRARIAN', 'USER']:

                return Response(
                    {
                        "error":
                        "Admin can only create librarians and users"
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

        elif creator.role == 'LIBRARIAN':

            if role != 'USER':

                return Response(
                    {
                        "error":
                        "Librarian can only create users"
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

        else:

            return Response(
                {
                    "error":
                    "You are not allowed to create users"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = RegisterSerializer(
            data=request.data
        )

        if serializer.is_valid():

            user = serializer.save()

            setup_link = (f"http://localhost:5174/create-password/"
                          f"{user.password_setup_token}")

            send_mail(subject="Library Management System - Account Setup",
                message=(
                    f"Hello {user.username},\n\n"
                    f"Your account has been created.\n\n"
                    f"Username: {user.username}\n\n"
                    f"Create Password:\n{setup_link}"
                ),
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False
            )

            if user.role == "USER":

                log_activity(
                    action="USER_CREATED",
                    description=(
                        f'User "{user.username}" created by '
                        f'{request.user.username}.'
                    ),
                    performed_by=request.user,
                )

            elif user.role == "LIBRARIAN":

                log_activity(
                    action="LIBRARIAN_CREATED",
                    description=(
                        f'Librarian "{user.username}" created by '
                        f'{request.user.username}.'
                    ),
                    performed_by=request.user,
                )
            return Response(
                        serializer.data,
                        status=status.HTTP_201_CREATED
                        )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        try:
            return User.objects.get(pk=pk)

        except User.DoesNotExist:
            return None

    def get(self, request, pk):

        if request.user.role not in ["ADMIN", "LIBRARIAN"]:

            return Response(
                {
                    "error": "You do not have permission to view user details"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        user = self.get_object(pk)

        if not user:

            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserSerializer(user)

        return Response(serializer.data)

    def put(self, request, pk):

        if request.user.role not in ["ADMIN", "LIBRARIAN"]:

            return Response(
                {
                    "error": "You do not have permission to update users"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        user = self.get_object(pk)

        if not user:

            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserSerializer(
            user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):

        if request.user.role not in ["ADMIN", "LIBRARIAN"]:

            return Response(
                {
                    "error": "You do not have permission to delete users"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        user = self.get_object(pk)

        if not user:

            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        user.delete()

        return Response(
            {"message": "User deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

class CreatePasswordAPIView(APIView):

    def post(self, request, token):

        try:

            user = User.objects.get(
                password_setup_token=token
            )

        except User.DoesNotExist:

            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CreatePasswordSerializer(
            data=request.data
        )

        if serializer.is_valid():

            user.set_password(
                serializer.validated_data['password']
            )

            user.password_setup_token = None

            user.save()

            PasswordHistory.objects.create(
                user=user,
                changed_by=user,
                reason="FIRST_PASSWORD"
            )

            return Response(
                {
                    "message":
                    "Password Created Successfully"
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginAPIView(APIView):

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        if serializer.is_valid():

            user = serializer.validated_data['user']

            refresh = RefreshToken.for_user(user)

            is_first_login = user.first_login

            if user.first_login:
                user.first_login = False
                user.save()

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "role": user.role,
                    "first_login": is_first_login,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class AdminDashboardAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "ADMIN":
            return Response(
                {
                    "error": "Only Admin can access this dashboard"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        total_librarians = User.objects.filter(
            role="LIBRARIAN"
        ).count()

        total_users = User.objects.filter(
            role="USER"
        ).count()

        total_books = Book.objects.aggregate(
            total=Sum("quantity")
        )["total"] or 0

        available_books = Book.objects.aggregate(
            total=Sum("available_quantity")
        )["total"] or 0

        issued_books = IssueBook.objects.filter(
            status="ISSUED"
        ).count()

        total_password_requests = PasswordResetRequest.objects.count()

        pending_password_requests = PasswordResetRequest.objects.filter(
            status="PENDING"
        ).count()

        # Deactivation Requests
        total_deactivation_requests = AccountDeactivationRequest.objects.count()

        pending_deactivation_requests = AccountDeactivationRequest.objects.filter(
            status="PENDING"
        ).count()

        return Response(
            {
                "Total_librarians": total_librarians,
                "Total_users": total_users,
                "Total_books": total_books,
                "Available_books": available_books,
                "Issued_books": issued_books,
                "Total_password_requests": total_password_requests,
                "Pending_password_requests": pending_password_requests,

                "Total_deactivation_requests": total_deactivation_requests,
                "Pending_deactivation_requests": pending_deactivation_requests,
                            },
            status=status.HTTP_200_OK
        )
    
class LibrarianAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != 'ADMIN':

            return Response(
                {"error":"Only admin can access"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        librarians = User.objects.filter(
            role='LIBRARIAN'
        )

        serializer = UserSerializer(librarians, many=True)

        return Response(serializer.data)

class NormalUserAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role not in ["ADMIN", "LIBRARIAN"]:

            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        users = User.objects.filter(
            role="USER"
        ).order_by("id")

        paginator = UserPagination()

        paginated_users = paginator.paginate_queryset(
            users,
            request
        )

        serializer = UserSerializer(
            paginated_users,
            many=True
        )

        return paginator.get_paginated_response(
            serializer.data
        )

class LibrarianDashboardAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "LIBRARIAN":
            return Response(
                {"error": "Only Librarian can access"},
                status=status.HTTP_403_FORBIDDEN
            )

        total_users = User.objects.filter(
            role="USER"
        ).count()

        total_books = Book.objects.aggregate(
            total=Sum("quantity")
        )["total"] or 0

        available_books = Book.objects.aggregate(
            total=Sum("available_quantity")
        )["total"] or 0

        issued_books = total_books - available_books

        total_password_requests = PasswordResetRequest.objects.count()

        pending_password_requests = PasswordResetRequest.objects.filter(
            status="PENDING"
        ).count()

        total_deactivation_requests = AccountDeactivationRequest.objects.count()

        pending_deactivation_requests = AccountDeactivationRequest.objects.filter(
            status="PENDING"
        ).count()

        return Response(
            {
                "Total_Users": total_users,
                "Total_Books": total_books,
                "Available_Books": available_books,
                "Issued_Books": issued_books,

                "Total_password_requests": total_password_requests,
                "Pending_password_requests": pending_password_requests,

                "Total_deactivation_requests": total_deactivation_requests,
                "Pending_deactivation_requests": pending_deactivation_requests,
            },
            status=status.HTTP_200_OK
        )
class UserDashboardAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "USER":
            return Response(
                {"error": "Only user can access"},
                status=status.HTTP_403_FORBIDDEN
            )

        user = request.user

        active_books = IssueBook.objects.filter(
            user=user,
            status="ISSUED"
        ).count()

        returned_books = IssueBook.objects.filter(
            user=user,
            status="RETURNED"
        ).count()

        total_fine = (
            IssueBook.objects.filter(user=user)
            .aggregate(total=Sum("fine_amount"))["total"] or 0
        )

        due_soon = IssueBook.objects.filter(
            user=user,
            status="ISSUED",
            due_date__lte=timezone.now().date() + timedelta(days=3)
        ).count()

        return Response(
            {
                "Username": user.username,
                "Email": user.email,
                "Active Books": active_books,
                "Returned Books": returned_books,
                "Total Fine": total_fine,
                "Due Soon": due_soon,
            },
            status=status.HTTP_200_OK,
        )

class ReportsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role not in [
            'ADMIN',
            'LIBRARIAN'
        ]:
            
            return Response(
                {"error":"Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        total_books = Book.objects.count()

        total_users = User.objects.filter(role='USER').count()

        total_librarians = User.objects.filter(role='LIBRARIAN').count()

        issued_books = IssueBook.objects.filter(status='ISSUED').count()

        returned_books = IssueBook.objects.filter(status='RETURNED').count()

        total_fine_collected = IssueBook.objects.aggregate(total=Sum('fine_amount'))['total'] or 0
        
        overdue_books = IssueBook.objects.filter(status='OVERDUE').count()


        return Response(
            {
                "Total Books": total_books,
                "Total Users": total_users,
                "Total Librarians": total_librarians,
                "Issued Books": issued_books,
                "Returned Books": returned_books,
                "Total Fine": total_fine_collected,
                "Overdue Books": overdue_books
            },
            status=status.HTTP_200_OK
        )

class ForgotPasswordAPIView(APIView):

    def post(self, request):

        serializer = ForgotPasswordSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        username = serializer.validated_data["username"]

        try:

            user = User.objects.get(
                username=username
            )

        except User.DoesNotExist:

            return Response(
                {
                    "error": "User not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        
        if PasswordResetRequest.objects.filter(
            user=user,
            status="PENDING"
        ).exists():

            return Response(
                {
                    "error": "A password reset request is already pending approval."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        PasswordResetRequest.objects.create(
            user=user
        )

        return Response(
            {
                "message": "Password reset request submitted successfully. Please wait for Admin/Librarian approval."
            },
            status=status.HTTP_200_OK
        )

class ResetPasswordAPIView(APIView):

    def post(self, request, token):

        try:

            user = User.objects.get(
                password_reset_token=token
            )

        except User.DoesNotExist:

            return Response(
                {
                    "error": "Invalid or expired reset link."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CreatePasswordSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(
            serializer.validated_data["password"]
        )

        user.password_reset_token = None

        user.save()

        password_request = PasswordResetRequest.objects.filter(
            user=user,
            status="APPROVED"
        ).order_by("-requested_at").first()

        if password_request:

            password_request.status = "COMPLETED"
            password_request.completed_at = timezone.now()
            password_request.save()

        PasswordHistory.objects.create(
            user=user,
            changed_by=user,
            reason="FORGOT_PASSWORD"
        )

        return Response(
            {
                "message": "Password reset successfully."
            },
            status=status.HTTP_200_OK
        )

class PasswordResetRequestListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role not in ["ADMIN", "LIBRARIAN"]:
            return Response(
                {
                    "error": "Permission denied."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        password_reset_requests= PasswordResetRequest.objects.select_related(
            "user"
        ).order_by("-requested_at")

        serializer = PasswordResetRequestSerializer(
           password_reset_requests,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class ApprovePasswordResetAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        if request.user.role not in ["ADMIN", "LIBRARIAN"]:
            return Response(
                {
                    "error": "Permission denied."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            password_request = PasswordResetRequest.objects.get(pk=pk)

        except PasswordResetRequest.DoesNotExist:

            return Response(
                {
                    "error": "Request not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if password_request.status != "PENDING":

            return Response(
                {
                    "error": "Request already processed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = password_request.user

        user.password_reset_token = uuid4()
        user.save()

        password_request.status = "APPROVED"
        password_request.approved_by = request.user
        password_request.approved_at = timezone.now()
        password_request.save()

        log_activity(
            action="PASSWORD_APPROVED",
            description=(
                f'Password reset approved for "{user.username}" '
                f'by {request.user.username}.'
            ),
            performed_by=request.user,
        )

        reset_link = (
                f"http://localhost:5174/reset-password/"
                f"{user.password_reset_token}"
            )

        send_mail(
            subject="Library Management System - Password Reset",
            message=(
                f"Hello {user.username},\n\n"
                f"Your password reset request has been approved.\n\n"
                f"Click the link below to reset your password:\n\n"
                f"{reset_link}\n\n"
                f"If you did not request this password reset, please ignore this email."
            ),
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response(
            {
                "message": "Password reset email sent successfully."
            },
            status=status.HTTP_200_OK
        )

class RejectPasswordResetAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        if request.user.role not in ["ADMIN", "LIBRARIAN"]:
            return Response(
                {
                    "error": "Permission denied."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            password_request = PasswordResetRequest.objects.get(pk=pk)

        except PasswordResetRequest.DoesNotExist:

            return Response(
                {
                    "error": "Request not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if password_request.status != "PENDING":

            return Response(
                {
                    "error": "Request already processed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        password_request.status = "REJECTED"
        password_request.save()

        log_activity(
            action="PASSWORD_REJECTED",
            description=(
                f'Password reset rejected for "{password_request.user.username}" '
                f'by {request.user.username}.'
            ),
            performed_by=request.user,
        )

        return Response(
            {
                "message": "Password reset request rejected."
            },
            status=status.HTTP_200_OK
        )
    

class AccountDeactivationRequestAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

       
        if request.user.role != "USER":
            return Response(
                {
                    "error": "Only users can request account deactivation."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        
        if AccountDeactivationRequest.objects.filter(
            user=request.user,
            status="PENDING"
        ).exists():

            return Response(
                {
                    "error": "You already have a pending deactivation request."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AccountDeactivationRequestSerializer(
            data=request.data
        )

        if serializer.is_valid():

            deactivation_request = serializer.save(
                user=request.user
            )

            log_activity(
                action="DEACTIVATION_REQUESTED",
                description=(
                    f'{request.user.username} requested account deactivation.'
                ),
                performed_by=request.user,
            )

            return Response(
                AccountDeactivationRequestSerializer(
                    deactivation_request
                ).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class DeactivationRequestListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role not in ["ADMIN", "LIBRARIAN"]:

            return Response(
                {
                    "error": "Permission denied."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # Admin can see all requests
        if request.user.role == "ADMIN":

            deactivation_requests = (
                AccountDeactivationRequest.objects
                .select_related("user")
                .order_by("-requested_at")
            )

        # Librarian can only see USER requests
        else:

            deactivation_requests = (
                AccountDeactivationRequest.objects
                .select_related("user")
                .filter(user__role="USER")
                .order_by("-requested_at")
            )

        serializer = AccountDeactivationRequestSerializer(
            deactivation_requests,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    

class ApproveDeactivationAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        if request.user.role not in ["ADMIN", "LIBRARIAN"]:
            return Response(
                {"error": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            deactivation_request = AccountDeactivationRequest.objects.get(pk=pk)

        except AccountDeactivationRequest.DoesNotExist:
            return Response(
                {"error": "Request not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if deactivation_request.status != "PENDING":

            return Response(
                {"error": "Request already processed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = deactivation_request.user

        
        if IssueBook.objects.filter(
            user=user,
            status="ISSUED"
        ).exists():

            return Response(
                {
                    "error": "User has issued books. Return all books before deactivation."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        
        total_fine = (
            IssueBook.objects.filter(user=user)
            .aggregate(total=Sum("fine_amount"))["total"] or 0
        )

        if total_fine > 0:

            return Response(
                {
                    "error": "User has pending fine. Clear the fine before deactivation."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

     
        user.is_active = False
        user.save()

       
        deactivation_request.status = "APPROVED"
        deactivation_request.approved_by = request.user
        deactivation_request.approved_at = timezone.now()
        deactivation_request.save()

        
        log_activity(
            action="USER_DEACTIVATED",
            description=(
                f'User "{user.username}" was deactivated by '
                f'{request.user.username}.'
            ),
            performed_by=request.user,
        )

        return Response(
            {
                "message": "Account deactivated successfully."
            },
            status=status.HTTP_200_OK
        )
    

class RejectDeactivationAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        if request.user.role not in ["ADMIN", "LIBRARIAN"]:
            return Response(
                {"error": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            deactivation_request = AccountDeactivationRequest.objects.get(pk=pk)

        except AccountDeactivationRequest.DoesNotExist:
            return Response(
                {"error": "Request not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if deactivation_request.status != "PENDING":
            return Response(
                {"error": "Request already processed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        deactivation_request.status = "REJECTED"
        deactivation_request.rejected_by = request.user
        deactivation_request.rejected_at = timezone.now()
        deactivation_request.save()

        log_activity(
            action="DEACTIVATION_REJECTED",
            description=(
                f'Account deactivation request of '
                f'"{deactivation_request.user.username}" '
                f'was rejected by {request.user.username}.'
            ),
            performed_by=request.user,
        )

        return Response(
            {
                "message": "Deactivation request rejected successfully."
            },
            status=status.HTTP_200_OK
        )