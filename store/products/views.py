from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponseRedirect, redirect
from django.views.generic import ListView, TemplateView

from common.views import TitleMixin

from .models import Basket, Product, ProductCategory


class IndexView(TitleMixin, TemplateView):
    template_name = "products/index.html"
    title = "Store"


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = "products/products.html"
    paginate_by = 3
    title = "Store -> Каталог"

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        if category_id:
            category = ProductCategory.objects.get(id=category_id)  # pyright: ignore
            products = Product.objects.filter(category=category)  # pyright: ignore
        else:
            products = super(ProductsListView, self).get_queryset()

        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context["categories"] = ProductCategory.objects.all()  # type: ignore
        context["category_id"] = self.kwargs.get("category_id")

        return context


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
