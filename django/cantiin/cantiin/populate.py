from products.models import Product



def drop_db():
	from django.db import connection
	cursor = connection.cursor()
	cursor.execute("DROP DATABASE %s;", [connection.settings_dict['NAME']])

def create_db():
	from django.db import connection
	cursor = connection.cursor()
	cursor.execute("CREATE DATABASE %s;", [connection.settings_dict['NAME']])

def drop_create_db():
	drop_db()
	create_db()



from django.contrib.auth.models import User

def populate_users():
	User.objects.all().delete()

	u = User(username = "tewyute",email = "",password = "7895") # 1
	u.save(using="testing")

	User.objects.create_user("abc","","123786") # 1
	User.objects.create_user("tyrhhbg","","tuasdghjkas") # 1


def populate_products():
	Product.objects.all().delete()
	u = User.objects.all()[0]
	u.save()
	#print(u.__dict__)
	Product.objects.create(name = "Android", 
		price = 5, in_stock = True, owner = u)	
	Product.objects.create(name = "Labtob", 
		price = 100, in_stock = True, owner = u)	
	Product.objects.create(name = "Computer", 
		price = 60, in_stock = True, owner = u)	
	Product.objects.create(name = "CPU", 
		price = 3, in_stock = False, owner = u)	
	Product.objects.create(name = "Suit", 
		price = 40, in_stock = True, owner = u)	
	Product.objects.create(name = "Meat", 
		price = 78, in_stock = True, owner = u)	

	p1 = Product(name = "Computer", 
		price = 60, in_stock = True, owner = u)
	p1.save()






