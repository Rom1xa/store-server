from django.shortcuts import render

from .models import Product, ProductCategory


def index(request):
    context = {
        "title": "Store",
    }
    return render(request, "products/index.html", context)


def products(request):
    context = {
        "title": "Store - Каталог",
        "products": Product.objects.all(),  # type: ignore
        "categories": ProductCategory.objects.all(),  # type: ignore
    }
    return render(request, "products/products.html", context=context)
