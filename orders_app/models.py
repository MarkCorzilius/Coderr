from django.db import models
from accounts_app.models import User
class Order(models.Model):
    customer_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="customer_orders"
    )
    business_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="business_orders"
    )
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()
    offer_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
