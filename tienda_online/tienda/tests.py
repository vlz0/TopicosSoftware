from django.test import TestCase
from django.urls import reverse
from .models import Product, Categoria
from django.core.files.uploadedfile import SimpleUploadedFile

class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Categoria.objects.create(nombre="Electronics")
        Product.objects.create(name="Producto 1", price=100.0, category=self.category)

    def test_product_creation(self):
        """Test if a product is created with the correct name and price"""
        product = Product.objects.get(name="Producto 1")
        self.assertEqual(product.name, "Producto 1")
        self.assertEqual(product.price, 100.0)
        self.assertEqual(product.category.nombre, "Electronics")
        
class HomeViewTest(TestCase):

    def setUp(self):
        self.category = Categoria.objects.create(nombre="Electronics")
        self.image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        Product.objects.create(name="Producto 1", price=100.0, category=self.category, image=self.image)
        Product.objects.create(name="Producto 2", price=200.0, category=self.category, image=self.image)

    def test_home_view(self):
        """Test the home view"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Producto 1")
        self.assertContains(response, "Producto 2")