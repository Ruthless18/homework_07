from django.shortcuts import render
from django.views.generic import DetailView

from .models import Desktop, Notebook, Category

def main_page(request):
    return render(request, 'base.html', {})


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


def store(request):
    categories = Category.objects.get_categories_in_side_bar()
    return render(request, 'store.html', {'categories': categories})