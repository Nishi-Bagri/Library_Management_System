from django.db import models

class Book(models.Model):

    serial_no = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    total_pages = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)
    available_quantity = models.PositiveIntegerField(default=1)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.is_available = self.available_quantity > 0

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
