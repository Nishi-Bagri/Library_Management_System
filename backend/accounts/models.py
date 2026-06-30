from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4


class User(AbstractUser):

    ROLE_CHOICES = (
        ('ADMIN','Admin'),
        ('LIBRARIAN','Librarian'),
        ('USER','User'),
    )

    role = models.CharField(max_length=20,choices=ROLE_CHOICES, default='USER')

    password_setup_token = models.UUIDField(default=uuid4,null=True,blank=True,unique=True)
    
    password_reset_token = models.UUIDField(null=True, blank=True, unique=True)

    first_login = models.BooleanField(default=True)

    def __str__(self):
        return self.username
    
class PasswordHistory(models.Model):

    REASON_CHOICES = [
        ("FIRST_PASSWORD", "First Password Creation"),
        ("FORGOT_PASSWORD", "Forgot Password"),
        ("ADMIN_RESET", "Admin Reset"),
        ("PASSWORD_CHANGED", "Password Changed"),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="password_history")

    changed_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="password_changed_records")

    changed_at = models.DateTimeField(auto_now_add=True)

    reason = models.CharField(max_length=30,choices=REASON_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.reason}"
    
class PasswordResetRequest(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("COMPLETED", "Completed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="password_reset_requests")

    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="PENDING")

    requested_at = models.DateTimeField(auto_now_add=True)

    approved_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="approved_password_requests")

    approved_at = models.DateTimeField(null=True,blank=True)

    rejection_reason = models.TextField( blank=True, null=True)

    completed_at = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"
    

class AccountDeactivationRequest(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    REASON_CHOICES = [
        ("NO_LONGER_USING", "No Longer Using Library"),
        ("MOVING", "Moving to Another City"),
        ("PRIVACY", "Privacy Concerns"),
        ("DUPLICATE", "Duplicate Account"),
        ("OTHER", "Other"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="deactivation_requests"
    )

    reason = models.CharField(
        max_length=50,
        choices=REASON_CHOICES
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_deactivations"
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    rejected_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rejected_deactivations"
    )

    rejected_at = models.DateTimeField(
        null=True,
        blank=True
    )

    requested_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-requested_at"]

    def __str__(self):
        return f"{self.user.username} - {self.status}"
    

