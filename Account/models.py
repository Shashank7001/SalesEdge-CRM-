from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import uuid

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("sales_executive", "Sales Executive"),
        ("accounts_manager", "Accounts Manager"),
        ("operations_lead", "Operations Lead"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"




class Lead(models.Model):
    SALES_STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("qualified", "Qualified"),
        ("lost", "Lost"),
        ("converted", "Converted"),
    ]
    ACCOUNTS_STATUS_CHOICES = [
        ("verified", "Verified"),
        ("unverified", "Unverified"),
        ("rejected", "Rejected"),
    ]
    OP_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
    ]

    STATUS_CHOICES = [
        ("unwanted", "Unwanted"),
        ("wanted", "Wanted"),
    ]
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    sales_status = models.CharField(max_length=20, choices=SALES_STATUS_CHOICES, default="new")
    accounts_status = models.CharField(max_length=20, choices=ACCOUNTS_STATUS_CHOICES, default="unverified")
    operations_status = models.CharField(max_length=20, choices=OP_STATUS_CHOICES, default="pending")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="wanted")
    source = models.CharField(max_length=255, blank=True, null=True)
    account_image = models.ImageField(upload_to='transactions/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="leads"
    )
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.status})"




