from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 

from .models import Book
from .serializers import BookSerializer

class BookAPIView(APIView):

    def get(self, request):

        books = Book.objects.all()

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    def post(self, request):

        if request.user.role not in['ADMIN','LIBRARIAN']:

            return Response(
                {"error": "Permission Denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

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
                {"error":"Book not Found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = BookSerializer(book, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):

        error = self.check_permissions(request)

        if error:
            return error

        book = self.get_object(pk)

        if not book:

            return Response(
                {"error":"Book not Found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        book.delete()

        return Response(
            {"message":"Book deleted Successfully"},
            status=status.HTTP_204_NO_CONTENT
        )