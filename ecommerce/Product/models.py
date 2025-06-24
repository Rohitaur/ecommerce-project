from django.db import models
from django.conf import settings
from Category.models import Category

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=200)

    brand = models.CharField(max_length=100, blank=True, default="")  # brand field added

    description = models.TextField(blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    is_active = models.BooleanField(default=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='products_created')

    created_at = models.DateTimeField(auto_now_add=True)

    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='products_updated')
    
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.name}--{self.description}--{self.is_active}"