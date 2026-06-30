from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 

from .models import Book
from .serializers import BookSerializer
from .pagination import BookPagination

from activity.utils import log_activity


class BookAPIView(APIView):

    def get(self, request):

        books = Book.objects.all().order_by("id")

        paginator = BookPagination()

        paginated_books = paginator.paginate_queryset(
            books,
            request
        )

        serializer = BookSerializer(paginated_books, many=True)

        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):

        print("===== BOOK POST CALLED =====")

        if request.user.role not in['ADMIN','LIBRARIAN']:

            print("Permission Denied")

            return Response(
                {"error": "Permission Denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():

            print("Serializer Valid")

            book = serializer.save()

            print("Book Saved:", book.title)

            log_activity(
                action="BOOK_ADDED",
                description=f'Book "{book.title}" was added.',
                performed_by=request.user,
            )
               
            print("Activity Logged Successfully")
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class BookDetailAPIView(APIView):

    def get_object(self, pk):

        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return None
        
    def check_permissions(self, request):
        
        if request.user.role not in ['ADMIN','LIBRARIAN']:

            return Response(
                {"error":"Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )
    
    def get(self, request, pk):

        book = self.get_object(pk)

        if not book:
            return Response(
                {"error":"Book not Found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = BookSerializer(book)

        return Response(serializer.data)
    
    def put(self, request, pk):

        error = self.check_permissions(request)

        if error:
            return error

        book = self.get_object(pk)

        if not book:
            return Response(
                {"error": "Book not Found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BookSerializer(
            book,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            updated_book = serializer.save()

            log_activity(
                action="BOOK_UPDATED",
                description=f'Book "{updated_book.title}" was updated by {request.user.username}.',
                performed_by=request.user,
            )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, pk):

        error = self.check_permissions(request)

        if error:
            return error

        book = self.get_object(pk)

        if not book:

            return Response(
                {"error": "Book not Found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Store title before deleting
        book_title = book.title

        book.delete()

        log_activity(
            action="BOOK_DELETED",
            description=f'Book "{book_title}" was deleted by {request.user.username}.',
            performed_by=request.user,
        )

        return Response(
            {"message": "Book deleted Successfully"},
            status=status.HTTP_204_NO_CONTENT
        )