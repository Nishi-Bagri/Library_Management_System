from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail

from books.models import Book
from transactions.models import IssueBook
from django.db.models import Sum

from .models import User
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    CreatePasswordSerializer,
    LoginSerializer
)


class UserAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        users = User.objects.all()

        serializer = UserSerializer(
            users,
            many=True
        )

        return Response(serializer.data)

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

            serializer.save()
            user = User.objects.get(username=serializer.validated_data['username'])

            setup_link = (
                f"http://127.0.0.1:8000/api/accounts/create-password/"
                f"{user.password_setup_token}/"
            )

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
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserDetailAPIView(APIView):

    def get_object(self, pk):

        try:
            return User.objects.get(pk=pk)

        except User.DoesNotExist:
            return None

    def get(self, request, pk):

        user = self.get_object(pk)

        if not user:

            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserSerializer(user)

        return Response(serializer.data)

    def put(self, request, pk):

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

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "role": user.role
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

        if request.user.role != 'ADMIN':

            return Response(
                {
                    "error":"Only Admin can access this dashboard"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        total_librarians = User.objects.filter(role='LIBRARIAN').count()

        total_users = User.objects.filter(role='USER').count()

        total_books = Book.objects.aggregate(
            total=Sum('quantity')
        )['total'] or 0

        available_books = Book.objects.aggregate(
            total=Sum('available_quantity')
        )['total'] or 0

        issued_books = IssueBook.objects.filter(
            status='ISSUED'
        ).count()

        return Response(
            {
                "Total_librarians": total_librarians,
                "Total_users": total_users,
                "Total_books": total_books,
                "Available_books": available_books,
                "Issued_books": issued_books,
            }, status=status.HTTP_200_OK
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

        if request.user.role != 'ADMIN':

            return Response(
                {"error": "Only admin can access"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        users = User.objects.filter(role='USER')

        serializer = UserSerializer(users, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class LibrarianDashboardAPIView(APIView):

    permission_classes =[IsAuthenticated]

    def get(self, request):

        if request.user.role != 'LIBRARIAN':

            return Response(
                {"error":"Only Librarian can access"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        total_users = User.objects.filter(
            role='USER'
        ).count()

        total_books = Book.objects.count()

        available_books = Book.objects.filter(is_available=True).count()

        issued_books = IssueBook.objects.filter(status='ISSUED').count()

        return Response(
            {
                "Total_Users": total_users,
                "Total_Books": total_books,
                "Available_Books": available_books,
                "Issued_Books": issued_books
            },
            status=status.HTTP_200_OK
        )

class UserDashboardAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != 'USER':

            return Response(
                {"error":"Only user can access"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user = request.user

        active_books = IssueBook.objects.filter(
            user=user,
            status = 'ISSUED'
        ).count()

        returned_books = IssueBook.objects.filter(user=user, status='RETURNED').count()

        total_fine = IssueBook.objects.filter(user=user).aggregate(total=Sum('fine_amount'))['total'] or 0

        return Response(
            {
                "Username": user.username,
                "Email": user.email,
                "Active Books": active_books,
                "Returned Books": returned_books,
                "Total Fine": total_fine
            },
            status=status.HTTP_200_OK
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
                "Total Fine Collected": total_fine_collected,
                "Overdue Books": overdue_books
            },
            status=status.HTTP_200_OK
        )