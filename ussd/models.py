from django.db import models
from django.utils import timezone

class Crop(models.Model):
    """Model for crop types available for trading"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    usdc_price = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        default=0,
        help_text="Current price in USDC per kg"
    )
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class User(models.Model):
    """Model for user accounts"""
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    mpesa_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    usdc_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rewards_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number


class Transaction(models.Model):
    """Model for tracking crop sales and purchases"""
    PAYMENT_CHOICES = [
        ('MPESA', 'M-Pesa'),
        ('USDC', 'USDC'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    tx_hash = models.CharField(
        max_length=66,
        blank=True,
        null=True,
        help_text="On-chain transaction hash for USDC payment"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Calculate total amount if not provided
        if not self.total_amount:
            self.total_amount = self.quantity * self.price_per_kg

        # Set completed_at timestamp if status is COMPLETED
        if self.status == 'COMPLETED' and not self.completed_at:
            self.completed_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.phone_number} - {self.crop.name} - {self.quantity}kg - {self.status}"
