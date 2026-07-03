from books.models import Book

def search_books(query):
    books = Book.objects.filter(title_icontains=query)

    if not books.exists():
        return []
    

    return[
        {
            "title": book.title,
            "author": book.autor,
            "available": book.avaialable_quantity,
        }
        
        for book in books
    ]