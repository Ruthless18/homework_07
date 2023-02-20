from django.shortcuts import render
from django.views.generic import DetailView, View

from .models import Desktop, Notebook, Category, LatestProducts
from .mixins import CategoryDetailMixin, ProductDetailMixin


class BaseView(View):

    def get(self, request, *args, **kwargs):
        products = LatestProducts.objects.get_products_for_mp('desktop', 'notebook')
        categories = Category.objects.get_categories_in_side_bar()
        context = {
            'categories': categories,
            'products': products
        }
        return render(request, 'base.html', context)


class ProductDetailView(DetailView):

    CT_MODEL_MODEL_CLASS = {
        'desktop': Desktop,
        'notebook': Notebook,
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)


    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'


def categories(request):
    categories = Category.objects.get_categories_in_side_bar()
    return render(request, 'categories.html', {'categories': categories})


class CategoryDetailView(ProductDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'