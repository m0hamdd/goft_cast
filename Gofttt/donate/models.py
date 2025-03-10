from django.db import models
from accounts.models import User

class Donate(models.Model):
    CURRENCY_CHOICES = (
        ("IRR", "ریال"),
        ("DOLLAR", "دلار"),
        ("EURO", "یورو"),
        ("POUND", "پوند"),
        ("IQD", "دینار عراق"),
        ("LIRA", "لیر ترکیه"),
    )

    STATUS_CHOICES = (
        ("pending", "در انتظار پرداخت"),
        ("success", "پرداخت موفق"),
        ("failed", "پرداخت ناموفق"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="donations")
    amount = models.PositiveBigIntegerField()
    currency = models.CharField(max_length=9, choices=CURRENCY_CHOICES, default="IRR")
    transaction_id = models.CharField(max_length=100, null=True, blank=True, unique=True)  # شناسه تراکنش
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")  # وضعیت تراکنش
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'کاربر {self.user.phone_number} - مبلغ {self.amount} {self.get_currency_display()} - وضعیت {self.get_status_display()}'

    class Meta:
        ordering = ('-date',)
        verbose_name = 'کمک مالی'
        verbose_name_plural = 'کمک‌های مالی'
