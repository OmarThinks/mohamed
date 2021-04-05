from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Product(models.Model):
	name = models.CharField(max_length=150)
	price = models.FloatField()
	in_stock = models.BooleanField(default=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
