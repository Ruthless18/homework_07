from django.shortcuts import render
from django.views.generic.detail import SingleObjectMixin

from .models import Category, LatestProducts


class CategoryDetailMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.get_categories_in_side_bar()
        return context


class ProductDetailMixin(SingleObjectMixin):

    def get(self, request, *args, **kwargs):
        products = LatestProducts.objects.get_products_for_mp('desktop', 'notebook')
        categories = Category.objects.get_categories_in_side_bar()
        context = {
            'categories': categories,
            'products': products
        }
        return render(request, 'category_detail.html', context)