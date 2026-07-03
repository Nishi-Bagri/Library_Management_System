from books.models import Book


def serialize_book(book):
    return {
        "id": book.id,
        "serial_no": book.serial_no,
        "title": book.title,
        "author": book.author,
        "category": book.category,
        "total_pages": book.total_pages,
        "quantity": book.quantity,
        "available_quantity": book.available_quantity,
        "is_available": book.is_available,
    }


def serialize_books(books):
    return [serialize_book(book) for book in books]


def search_books(query):
    books = Book.objects.filter(title__icontains=query)

    if not books.exists():
        return []

    return serialize_books(books)


def available_books():
    books = Book.objects.filter(available_quantity__gt=0)

    return serialize_books(books)


def search_by_author(author):
    books = Book.objects.filter(author__icontains=author)

    if not books.exists():
        return []

    return serialize_books(books)


def search_by_category(category):
    books = Book.objects.filter(category__icontains=category)

    if not books.exists():
        return []

    return serialize_books(books)


def book_details(title):
    try:
        book = Book.objects.get(title__iexact=title)
        return serialize_book(book)

    except Book.DoesNotExist:
        return {}