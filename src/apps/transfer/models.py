from django.db import models


class TransferState(models.TextChoices):
    CREATED = "created", "created"
    CONFIRMED = "confirmed", "confirmed"
    CANCELLED = "cancelled", "cancelled"


class Transfer(models.Model):

    ext_id = models.CharField(max_length=100, unique=True)

    sender_card_number = models.CharField(max_length=16)
    receiver_card_number = models.CharField(max_length=16)

    sender_card_expiry = models.CharField(max_length=5)

    sender_phone = models.CharField(max_length=13, null=True, blank=True)
    receiver_phone = models.CharField(max_length=13, null=True, blank=True)

    sending_amount = models.DecimalField(max_digits=12, decimal_places=2)

    currency = models.IntegerField()

    receiving_amount = models.DecimalField(max_digits=12, decimal_places=2)

    state = models.CharField(
        max_length=20,
        choices=TransferState.choices,
        default=TransferState.CREATED
    )

    try_count = models.IntegerField(default=0)

    otp = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ext_id
    

class Error(models.Model):
    code = models.IntegerField(unique=True)
    en = models.CharField(max_length=255)
    ru = models.CharField(max_length=255)
    uz = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code}"
    
