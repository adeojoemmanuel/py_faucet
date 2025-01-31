from django.db import models

class Transaction(models.Model):
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    STATUS_CHOICES = [
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
    ]
    
    wallet_address = models.CharField(max_length=42)
    tx_hash = models.CharField(max_length=66)
    amount = models.DecimalField(max_digits=18, decimal_places=8)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet_address} - {self.amount}"