from django.urls import path

from .views import BaseView, ProductDetailView, categories, CategoryDetailView


urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    # Тут должна быть ссылка на выбор категои
    path('categories/', categories, name='categories'),
    # Тут должена быть конечная ссылка на категорию с товарами
    path('category/<str:slug>', CategoryDetailView.as_view(), name='category_detail'),
]
