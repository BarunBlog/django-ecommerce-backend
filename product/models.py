from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(default=0, max_digits=20, decimal_places=2, help_text='UNIT is BDT')
    image = models.ImageField(upload_to='product/')
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="rating must be greater than or equal to 1"),
            MaxValueValidator(5, message="rating must be less than or equal to 5")
        ]
    )
    description = models.TextField()
    verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.product}"
