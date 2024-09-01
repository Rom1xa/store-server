from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.contrib.auth.decorators import login_required

from .models import Basket, Product, ProductCategory


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
    return render(request, "products/products.html", context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)  # type: ignore

    try:
        basket = Basket.objects.get(user=request.user, product=product)  # type: ignore
        basket.quantity += 1
        basket.save()
    except ObjectDoesNotExist:
        Basket.objects.create(product=product, user=request.user, quantity=1)  # type: ignore

    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def basket_remove(request, basket_id):
    basket_item = Basket.objects.filter(id=basket_id, user=request.user).first()
    if basket_item is not None:
        basket_item.delete()
    return redirect(to=request.META["HTTP_REFERER"])
