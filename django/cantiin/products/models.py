from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Product(models.Model):
	name = models.CharField(max_length=150)
	price = models.FloatField()
	in_stock = models.BooleanField(default=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	
	def __str__(self):
		return f"{self.id}) {self.name} : {str(self.in_stock)}"





def populate_prodcuts():
	Product.objects.all().delete()
	p1 = Product.objects.create(name = "Android", price = 5, 
		in_stock = True, owner = 1)




#populate_prodcuts()
