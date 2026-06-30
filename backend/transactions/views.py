from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import IssueBook
from .serializers import IssueBookSerializer, FineHistorySerializer, FineSummarySerializer
from accounts.models import User

from django.db.models import Sum, Count

from activity.utils import log_activity


from rest_framework.permissions import IsAuthenticated

from datetime import timedelta
from django.utils import timezone

class MyBooksAPIView(APIView):

    permission_classes= [IsAuthenticated]

    def get(self, request):

        if request.user.role != "USER":
            return Response(
                {"error": "Only users can access this."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        books = IssueBook.objects.filter(
            user= request.user).order_by("-issue_date")
        
        serializer = IssueBookSerializer(books, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class IssueBookAPIView(APIView):

    def get(self, request):
        issue_books = IssueBook.objects.all().order_by("id")
        serializer = IssueBookSerializer(issue_books, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = IssueBookSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.validated_data["user"]
            book = serializer.validated_data["book"]

        
            active_books = IssueBook.objects.filter(
                user=user,
                status="ISSUED"
            ).count()

            if active_books >= 3:
                return Response(
                    {
                        "error": "User has already issued the maximum of 3 books."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

    
            overdue_book = IssueBook.objects.filter(
                user=user,
                status="ISSUED",
                due_date__lt=timezone.now().date()
            ).exists()

            if overdue_book:
                return Response(
                    {
                        "error": "User has an overdue book. Return it before issuing another book."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            
            same_book = IssueBook.objects.filter(
                user=user,
                book=book,
                status="ISSUED"
            ).exists()

            if same_book:
                return Response(
                    {
                        "error": "This book is already issued to the user."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

           
            if book.available_quantity <= 0:

                return Response(
                    {
                        "error": "Book not available."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            book.available_quantity -= 1

            if book.available_quantity == 0:
                book.is_available = False

            book.save()

            due_date = timezone.now().date() + timedelta(days=15)

            issue_book = serializer.save(
                issued_by= request.user,
                due_date=due_date,
                status="ISSUED"
            )

            issue_book.issue_number = f"ISS-{issue_book.id:05d}"
            issue_book.save()

            log_activity(
                action="BOOK_ISSUED",
                 description=(
                    f'Book "{book.title}" issued to {user.username} '
                    f'by {request.user.username}. '
                    f'Issue No: {issue_book.issue_number}'
                ),
                performed_by=request.user,
            )

            return Response(
                IssueBookSerializer(issue_book).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
    )


class IssueBookDetailAPIView(APIView):

    def get_object(self, pk):

        try:
            return IssueBook.objects.get(pk=pk)
        except IssueBook.DoesNotExist:
            return None
        
    def get_issue_book(self, pk):

        issue_book = self.get_object(pk)

        if not issue_book:
            return None, Response(
                {"error":"Issue record not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return issue_book, None
        
    def get(self, request, pk):

        issue_book, error = self.get_issue_book(pk)

        if error:
            return error

        serializer = IssueBookSerializer(issue_book)

        return Response(serializer.data)
    
    def put(self, request, pk):

        issue_book, error = self.get_issue_book(pk)

        if error:
            return error


        serializer = IssueBookSerializer(issue_book, data=request.data, partial=True)

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

        issue_book, error = self.get_issue_book(pk)

        if error:
            return error
        
        issue_book.delete()

        return Response(
            {"message":"Issue record deleted successfully"},
            status= status.HTTP_204_NO_CONTENT
        )

class ReturnBookAPIView(APIView):

    def post(self, request, pk):

        try:
            issue_book = IssueBook.objects.get(pk=pk)

        except IssueBook.DoesNotExist:
            return Response(
                {"error": "Issue record not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if issue_book.status == "RETURNED":
            return Response(
                {"error": "Book already returned"},
                status=status.HTTP_400_BAD_REQUEST
            )

        issue_book.actual_return_date = timezone.now().date()

       
        if issue_book.actual_return_date > issue_book.due_date:

            late_days = (
                issue_book.actual_return_date - issue_book.due_date
            ).days

            issue_book.late_days = late_days

            issue_book.fine_amount = (
                late_days * issue_book.fine_per_day
            )

            fine_collected = request.data.get(
                "fine_collected",
                False
            )

            if not fine_collected:

                return Response(
                    {
                        "overdue": True,
                        "late_days": late_days,
                        "fine_per_day": issue_book.fine_per_day,
                        "fine_amount": issue_book.fine_amount,
                        "message": "Collect the fine before returning the book."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        
        book = issue_book.book

        book.available_quantity += 1
        book.is_available = True
        book.save()

       
        issue_book.status = "RETURNED"
        issue_book.save()

        
        log_activity(
            action="BOOK_RETURNED",
            description=(
                f'Book "{book.title}" returned by '
                f'{issue_book.user.username} and received by '
                f'{request.user.username}.'
            ),
            performed_by=request.user,
        )

        
        if issue_book.fine_amount > 0:

            log_activity(
                action="FINE_COLLECTED",
                description=(
                    f'₹{issue_book.fine_amount} fine collected '
                    f'from {issue_book.user.username} by '
                    f'{request.user.username}.'
                ),
                performed_by=request.user,
            )

        return Response(
            {
                "message": "Book returned successfully"
            },
            status=status.HTTP_200_OK
        )
class RenewBookAPIView(APIView):

    def post(self, request, pk):

        try:
            issue_book = IssueBook.objects.get(pk=pk)
        except IssueBook.DoesNotExist:

            return Response(
                {"error":"Issue record not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if issue_book.status == 'RETURNED':

            return Response(
                {"error":"Book already returned"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if issue_book.renewal_count >=1:

            return Response(
                {"error":"Renewal limit exceeded"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        issue_book.due_date +=timedelta(days=15)

        issue_book.renewal_count +=1

        issue_book.save()

        log_activity(
            action="BOOK_RENEWED",
            description=(
                f'Book "{issue_book.book.title}" renewed for '
                f'{issue_book.user.username} by {request.user.username}.'
            ),
            performed_by=request.user,
        )

        return Response(
            {"message":"Book renewed successfully"},
            status=status.HTTP_200_OK
        )

class UserSummaryAPIView(APIView):

    def get(self, request, user_id):

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:

            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        active_books = IssueBook.objects.filter(
            user=user,
            status="ISSUED"
        )

        overdue_books = active_books.filter(
            due_date__lt=timezone.now().date()
        )

        return Response({
            "books_issued": active_books.count(),
            "remaining_limit": 3 - active_books.count(),
            "overdue_books": overdue_books.count()
        })
    

class FineSummaryAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role not in ["ADMIN", "LIBRARIAN"]:

            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        summary = (
            IssueBook.objects
            .filter(fine_amount__gt=0)
            .values(
                "user",
                "user__username"
            )
            .annotate(
                books_with_fine=Count("id"),
                total_fine=Sum("fine_amount")
            )
            .order_by("-total_fine")
        )

        serializer = FineSummarySerializer(
            summary,
            many=True
        )

        total_fine_collected = (
            IssueBook.objects.filter(
                fine_amount__gt=0
            ).aggregate(
                total=Sum("fine_amount")
            )["total"] or 0
        )

        users_with_fine = summary.count()

        total_fined_books = (
            IssueBook.objects.filter(
                fine_amount__gt=0
            ).count()
        )

        return Response(
            {
                "total_fine_collected": total_fine_collected,
                "users_with_fine": users_with_fine,
                "total_fined_books": total_fined_books,
                "results": serializer.data,
            }
        )
    
class FineHistoryAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):

        if request.user.role not in ["ADMIN", "LIBRARIAN"]:

            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        history = IssueBook.objects.filter(
            user_id=user_id,
            fine_amount__gt=0
        ).select_related(
            "book"
        ).order_by("-actual_return_date")

        serializer = FineHistorySerializer(
            history,
            many=True
        )

        total_fine = history.aggregate(
            total=Sum("fine_amount")
        )["total"] or 0

        return Response(
            {
                "total_fine": total_fine,
                "history": serializer.data,
            },
            status=status.HTTP_200_OK
        )