from django.db import models
from accounts.models import User
from books.models import Book

class IssueBook(models.Model):
  
  STATUS_CHOICES = (
    ('ISSUED', 'Issued'),
    ('RETURNED', 'Returned'),
    ('OVERDUE', 'Overdue'),
  )

  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_books')

  book = models.ForeignKey(Book, on_delete=models.CASCADE)

  issue_number = models.CharField(max_length=20, unique=True, null=True, blank=True, )

  issued_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issued_books')

  issue_date = models.DateField(auto_now_add=True)

  due_date = models.DateField()

  actual_return_date = models.DateField(null=True, blank=True)

  renewal_count = models.PositiveIntegerField(default=0)

  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ISSUED')

  late_days = models.PositiveIntegerField(default=0)

  fine_per_day = models.DecimalField(max_digits=6, decimal_places=2, default=10.00)

  fine_amount = models.DecimalField(max_digits = 10,decimal_places=2,default=0)

  created_at = models.DateTimeField(auto_now_add=True)

  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.user.username} - {self.book.title}"
  
