from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.contrib.auth.decorators import login_required

from .models import Basket, Product, ProductCategory
from django.core.paginator import Paginator


def index(request):
    context = {
        "title": "Store",
    }
    return render(request, "products/index.html", context)


def products(request, category_id=None):
    PER_PAGE = 3

    if category_id:
        category = ProductCategory.objects.get(id=category_id)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    page = request.GET.get("page", 1)
    if not isinstance(page, int):
        if page.isdigit():
            page = int(page)
        else:
            page = 1

    paginator = Paginator(products, per_page=PER_PAGE)
    page_products = paginator.page(page)

    return render(
        request,
        "products/products.html",
        context={
            "title": "Store - продукты",
            "products": page_products,
            "categories": ProductCategory.objects.all(),
            "category_id": category_id,
        },
    )


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
