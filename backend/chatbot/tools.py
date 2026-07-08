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
    

def library_information(topic):
    """
    Return library-related information based on the requested topic.
    """

    topic = topic.lower().strip()

    information = {
        "fine": (
            "A fine of ₹10 per day is charged for each day a book is returned "
            "after its due date."
        ),

        "borrow": (
            "Users can borrow books from the library through the librarian. "
            "Books are issued based on availability."
        ),

        "renew": (
            "Books can be renewed before the due date, subject to library "
            "rules and availability."
        ),

        "timings": (
            "The library is open from Monday to Friday, "
            "9:00 AM to 6:00 PM."
        ),

        "contact": (
            "For assistance, please contact the librarian or the "
            "library administrator."
        ),

        "password": (
            "If you forget your password, use the 'Forgot Password' option "
            "on the login page or contact the librarian/administrator."
        ),
    }

    for key, value in information.items():
        if key in topic:
            return {
                "topic": key,
                "information": value,
            }

    return {
        "topic": "general",
        "information": (
            "I can help with library policies such as fines, borrowing, "
            "renewal, library timings, contact information, and password reset."
        ),
    }

def recommend_books(category):
    """
    Recommend books based on category.
    """

    books = Book.objects.filter(
        category__icontains=category,
        available_quantity__gt=0
    )[:5]

    if not books.exists():
        return []

    return serialize_books(books)