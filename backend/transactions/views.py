from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import IssueBook
from .serializers import IssueBookSerializer

from datetime import timedelta
from django.utils import timezone

class IssueBookAPIView(APIView):

    def get(self, request):
        issue_books = IssueBook.objects.all()
        serializer = IssueBookSerializer(issue_books, many=True)
        return Response(serializer.data)
    
    def post(self, request):

        serializer = IssueBookSerializer(data=request.data)

        if serializer.is_valid():
            
            book = serializer.validated_data['book']

            if book.available_quantity <= 0 :

                return Response(
                    {"error":"Book not available"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            book.available_quantity -= 1

            if book.available_quantity == 0 :
                book.is_available = False

            book.save()
            
            due_date = (timezone.now().date() + timedelta(days=15) )

            issue_book = serializer.save(
                issued_by=request.user,
                due_date=due_date,
                status='ISSUED'
            ) 

            return Response(IssueBookSerializer(issue_book).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
                {"error":"Issue record not found"},
                status=status.HTTP_404_NOT_FOUND
            )    
        
        if issue_book.status == 'RETURNED':

            return Response(
                {"error":"Book already returned"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
        book = issue_book.book

        book.available_quantity +=1

        book.is_available = True

        book.save()

        issue_book.actual_return_date = (
            timezone.now().date()
        )

        if issue_book.actual_return_date > issue_book.due_date:

            late_days = (
                issue_book.actual_return_date - issue_book.due_date
            ).days

            issue_book.late_days = late_days

            issue_book.fine_amount = late_days * 10

        issue_book.status = 'RETURNED'

        issue_book.save()

        return Response(
            {"message":"Book returned successfully"},
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

        return Response(
            {"message":"Book renewed successfullt"},
            status=status.HTTP_200_OK
        )