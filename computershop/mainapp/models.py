from django.db import models


# Главная -> Computer_system
class Computer_system(models.Model):
    name = models.CharField(max_length=64, unique=True)


    def __str__(self):
        return f'{self.name}'

# Computer_system -> Category(Desktop Computers, Notebooks/Laptops, Peripherals)
class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    category = models.ForeignKey(Computer_system, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.name} ({self.category})'

# Category -> Product(INWI, WELL, PacMan)
class Product(models.Model):
    name = models.CharField(max_length=64)
    price = models.IntegerField(verbose_name='price')
    description = models.CharField(verbose_name='description', max_length=64, blank=True)
    specs = models.TextField(blank=True)
    category = models.OneToOneField(Category, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.name} {self.price} {self.description} {self.specs} ({self.category.name})'

# Product -> Accessories(Temperature info, DVI, Charger)
class Accessories(models.Model):
    name = models.CharField(max_length=64, unique=True)
    price = models.IntegerField(verbose_name='price')
    products = models.ManyToManyField(Product)


    def __str__(self):
        return f'{self.name} {self.price} ({self.products})'