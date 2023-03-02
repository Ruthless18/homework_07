from django.urls import path

from .views import (
    BaseView,
    ProductDetailView,
    CategoriesView,
    CategoryDetailView,
    CartView,
    AddToCartView,
    DeleteFromCartView,
    ChangeQTYView,
    CheckoutView,
    MakeOrderView,
)


urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    # Тут должна быть ссылка на выбор категои
    path('categories/', CategoriesView.as_view(), name='categories'),
    # Тут должена быть конечная ссылка на категорию с товарами
    path('category/<str:slug>', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('delete-from-cart/<str:ct_model>/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-quality/<str:ct_model>/<str:slug>/', ChangeQTYView.as_view(), name='change_quality'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),
]
