from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(default=0, max_digits=20, decimal_places=2, help_text='UNIT is BDT')
    image = models.ImageField(upload_to='product/')
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
