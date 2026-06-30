from django.db import models
from accounts.models import User


class Activity(models.Model):

    ACTION_CHOICES = [
        ("BOOK_ADDED", "Book Added"),
        ("BOOK_UPDATED", "Book Updated"),
        ("BOOK_DELETED", "Book Deleted"),
        ("BOOK_ISSUED", "Book Issued"),
        ("BOOK_RETURNED", "Book Returned"),
        ("BOOK_RENEWED", "Book Renewed"),
        ("USER_CREATED", "User Created"),
        ("LIBRARIAN_CREATED", "Librarian Created"),
        ("PASSWORD_APPROVED", "Password Approved"),
        ("PASSWORD_REJECTED", "Password Rejected"),
        ("FINE_COLLECTED", "Fine Collected"),
        ("DEACTIVATION_REQUESTED", "Deactivation Requested"),
        ("USER_DEACTIVATED", "User Deactivated"),
        ("DEACTIVATION_REJECTED", "Deactivation Rejected"),
    ]

    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES
    )

    description = models.TextField()

    performed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="activities"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} - {self.description}"
