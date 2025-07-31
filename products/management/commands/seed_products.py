# from django.core.management.base import BaseCommand
# from products.models import Category, Product

# class Command(BaseCommand):
#     help = 'Seed initial categories and products'

#     def handle(self, *args, **kwargs):
#         # Create categories
#         electronics, _ = Category.objects.get_or_create(name='Electronics')
#         books, _ = Category.objects.get_or_create(name='Books')
#         clothing, _ = Category.objects.get_or_create(name='Clothing')

#         # Create products
#         Product.objects.get_or_create(name='Smartphone', price=50000, stock=10, category=electronics)
#         Product.objects.get_or_create(name='Laptop', price=85000, stock=5, category=electronics)
#         Product.objects.get_or_create(name='Django for Beginners', price=500, stock=20, category=books)
#         Product.objects.get_or_create(name='T-Shirt', price=700, stock=50, category=clothing)

#         self.stdout.write(self.style.SUCCESS("✅ Categories and Products seeded successfully."))
