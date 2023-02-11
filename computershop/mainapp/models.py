from PIL import Image
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse


User = get_user_model()


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass


class MaxSizeErrorException(Exception):
    pass


# Весь список товаров на главной
class LatestProductManager:

    @staticmethod
    def get_products_for_mp(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(products, key=lambda x: x.__class__._meta.model.name.startswith(with_respect_to), reverse=True)
        return products

class LatestProducts:

    objects = LatestProductManager()


class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Персональные компьютеры': 'desktop__count',
        'Ноутбуки': 'notebook__count',
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_in_side_bar(self):
        models = get_models_for_count('desktop', 'notebook')
        qs = list(self.get_queryset().annotate(*models).values())
        return [dict(id=c['id'], name=c['name'], slug=c['slug'], count=c[self.CATEGORY_NAME_COUNT_NAME[c['name']]]) for c in qs]


# Category(Desktop Computers, Notebooks, Peripherals)
class Category(models.Model):

    name = models.CharField(max_length=128, unique=True, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name


# Product(INWI, WELL, PacMan)
class Product(models.Model):

    MIN_VALID_RESOLUTION = (300, 300)
    MAX_VALID_RESOLUTION = (2000, 2000)
    MAX_VALID_IMAGE_SIZE = 3145728

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image_01 = models.ImageField(verbose_name='Изображение 1')
    image_02 = models.ImageField(verbose_name='Изображение 2')
    image_03 = models.ImageField(verbose_name='Изображение 3')
    image_04 = models.ImageField(verbose_name='Изображение 4')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    discount = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='Процент скидки')
    description = models.TextField(verbose_name='Описание', null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        images = [self.image_01, self.image_02, self.image_03, self.image_04]
        for image in images:
            img = Image.open(image)
            min_height, min_width = self.MIN_VALID_RESOLUTION
            max_height, max_width = self.MAX_VALID_RESOLUTION
            if image.size > self.MAX_VALID_IMAGE_SIZE:
                raise MaxSizeErrorException('Размер изображения не должен превышать 3MB!')
            if img.height < min_height or img.width < min_width:
                raise MinResolutionErrorException('Изображение не соответствует требованиям!')
            if img.height > max_height or img.width > max_width:
                raise MaxResolutionErrorException('Изображение не соответствует требованиям!')
            super().save(*args, **kwargs)

    def discount_price_product(self):
        if self.discount > 0:
            discount_end = self.price - self.price * self.discount / 100
            return discount_end
        return self.price


    discount_price = discount_price_product

class Desktop(Product):

    brand = models.CharField(max_length=255, verbose_name='Производитель')
    model = models.CharField(max_length=128, verbose_name='Модель')
    form_factor = models.CharField(max_length=64, verbose_name='Форм-фактор корпуса')
    color = models.CharField(max_length=64, verbose_name='Цвет')
    os = models.CharField(max_length=128, verbose_name='Операционная система')
    cpu = models.CharField(max_length=255, verbose_name='Процессор')
    gpu = models.CharField(max_length=255, verbose_name='Видеокарта')
    motherboard = models.CharField(max_length=255, verbose_name='Материнская плата')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    ssd = models.CharField(max_length=255, verbose_name='Твердотельный накопитель')
    hdd = models.CharField(max_length=255, verbose_name='НЖМД')
    psu = models.CharField(max_length=255, verbose_name='Блок питания')
    case = models.CharField(max_length=255, verbose_name='Корпус')
    dimension = models.CharField(max_length=255, verbose_name='Габариты ШхВхГ')
    wifi = models.BooleanField(default=True, verbose_name='Wi-Fi')
    bluetooth = models.BooleanField(default=True, verbose_name='Bluetooth')
    rgb = models.BooleanField(default=True, verbose_name='Подсветка')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.name)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')

    # def da_net(self):
    #     fields = [self.wifi, self.bluetooth, self.rgb]
    #     for field in fields:
    #         if field == boolResult:
    #             return field(str('Да'))
    #         else:
    #             return field = 'Нет'


class Notebook(Product):

    brand = models.CharField(max_length=255, verbose_name='Производитель')
    model = models.CharField(max_length=128, verbose_name='Модель')
    color = models.CharField(max_length=64, verbose_name='Цвет')
    diagonal = models.CharField(max_length=64, verbose_name='Диагональ')
    screen_resolution = models.CharField(max_length=64, verbose_name='Разрешение экрана')
    display_type = models.CharField(max_length=64, verbose_name='Тип дисплея')
    os = models.CharField(max_length=128, verbose_name='Операционная система')
    cpu = models.CharField(max_length=255, verbose_name='Процессор')
    gpu = models.CharField(max_length=255, verbose_name='Видеокарта')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    ssd = models.CharField(max_length=255, verbose_name='Твердотельный накопитель')
    hdd = models.CharField(max_length=255, verbose_name='НЖМД')
    battery = models.CharField(max_length=255, verbose_name='Аккумулятор')
    dimension = models.CharField(max_length=255, verbose_name='Габариты ШхВхГ')
    web_cam = models.BooleanField(default=True, verbose_name='Веб-камера')
    wifi = models.BooleanField(default=True, verbose_name='Wi-Fi')
    bluetooth = models.BooleanField(default=True, verbose_name='Bluetooth')
    rgb = models.BooleanField(default=True, verbose_name='Подсветка')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.name)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')

class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quality = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return "Продукт: {} (для корзины)". format(self.content_object.name)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=255, verbose_name='Номер телефона')

    def __str__(self):
        return f'{self.user.first_name, self.user.last_name}'