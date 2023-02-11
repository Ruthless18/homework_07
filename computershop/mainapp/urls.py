from django.urls import path

from .views import main_page, ProductDetailView, store


urlpatterns = [
    path('', main_page, name='base'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('store/', store, name='store'),
]
