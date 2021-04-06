from django.test import TestCase

# Create your tests here.



from django.test import TestCase
from product.models import Product




class ProductTestCase(TestCase):
	def setUp(self):

	def test_animals_can_speak(self):
		"""Animals that can speak are correctly identified"""
		lion = Animal.objects.get(name="lion")
		cat = Animal.objects.get(name="cat")
		self.assertEqual(lion.speak(), 'The lion says "roar"')
		self.assertEqual(cat.speak(), 'The cat says "meow"')





