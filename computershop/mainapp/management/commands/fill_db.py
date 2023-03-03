# from django.core.management.base import BaseCommand, CommandError
# from mainapp.models import Computer_system, Category, Product, Accessories
#
# class Command(BaseCommand):
#     help = 'Fill db'
#
#     def handle(self, *args, **options):
#
#         """
#         удаление старых данных
#         """
#         Computer_system.objects.all().delete()
#         Category.objects.all().delete()
#         Product.objects.all().delete()
#         Accessories.objects.all().delete()
#
#         """
#         создаем новые данные
#         """
#         print('Создание новых данных')
#
#         # Главная -> Computer_system(Desktop Systems, Portable Systems)
#         computer_system1 = Computer_system.objects.create(name='Desktop Systems')
#         computer_system2 = Computer_system.objects.create(name='Portable Systems')
#         computer_systems = Computer_system.objects.all()
#         print(computer_systems)
#         print('---------ALL computer_systems------------')
#         for computer_system in computer_systems:
#             print(computer_system.name)
#         print('---------END computer_systems------------')
#
#         # Computer_system(Desktop Systems, Portable Systems) -> Category(Desktop Computers, Notebooks/Laptops, Peripherals)
#         category_cs1 = Category.objects.create(name='Desktops', category=computer_system1)
#         category_cs2 = Category.objects.create(name='Notebooks/Laptops', category=computer_system2)
#         category_cs3 = Category.objects.create(name='Peripherals', category=computer_system1)
#         categories = Category.objects.all()
#         print(categories)
#         print('---------ALL categories------------')
#         for category in categories:
#             print(category.name)
#         print('---------END categories------------')
#
#         # Category -> Product(INWI, WELL, PacMan)
#         product1 = Product.objects.create(name='INWI', price=1000, category=category_cs1)
#         product2 = Product.objects.create(name='WELL', price=10000, category=category_cs2)
#         product3 = Product.objects.create(name='Charge adapter', price=30, category=category_cs3)
#         products = Product.objects.all()
#         print(products)
#
#         # Фильтры
#
#         products = Product.objects.filter(name='WELL')
#         print(products)
