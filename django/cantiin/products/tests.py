# python manage.py test
from django.contrib.auth.models import User
from products.models import Product


from cantiin.populate import (
delete_users, delete_products, delete_all_records,
populate_products ,populate_users ,populate_all)

from unittest import TestCase

class AllWorkingTestCase(TestCase):
	def test_case1(self):
		print("Test cases abouta start")
	

class populate_usersTestCase(TestCase):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg
		

		


