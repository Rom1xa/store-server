from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):  # type: ignore
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to="products_images")
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    def __str__(self):  # type: ignore
        return f"{self.category}: {self.name}"
