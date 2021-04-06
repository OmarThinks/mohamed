from django.test import TestCase
#from unittest import TestCase

# Create your tests here.



from django.test import SimpleTestCase, TransactionTestCase, LiveServerTestCase
from products.models import Product

from cantiin.populate import (populate_products,populate_users)

from django.test.runner import DiscoverRunner


import unittest

#print(SimpleTestCase.settings())
class ProductTestCase(unittest.TestCase):
	

	def setUp(self):
		populate_users()
		populate_products()
	def tearDown():
		pass
	
	def test_case1(self):
		#populate_users()
		#populate_products()
		print("first_test_case")
	





# run_tests()
