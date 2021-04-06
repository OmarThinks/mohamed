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
	User.objects.using("testing").all().delete()

	# 1
	User.objects.using("testing").create(
	username = "user1",email = "",password = "7895") # 1
	# 2
	User.objects.using("testing").create(username = "user2",
	email = "", password = "123786") # 2
	# 3
	User.objects.using("testing").create(username = "user3",
	email ="",password = "tuasdghjkas") # 3





def populate_products():
	Product.objects.using("testing").all().delete()
	
	all_users = User.objects.using("testing"
		).order_by('-id').all() 
	u1 = all_users[0]
	u2 = all_users[1]
	u3 = all_users[2]

	
	# 1
	Product.objects.using("testing").create(name = "Android", 
		price = 5, in_stock = True, owner = u1)	
	# 2
	Product.objects.using("testing").create(name = "Labtob", 
		price = 100, in_stock = True, owner = u2)	
	# 3
	Product.objects.using("testing").create(name = "Computer", 
		price = 60, in_stock = True, owner = u1)	
	# 4
	Product.objects.using("testing").create(name = "CPU", 
		price = 3, in_stock = False, owner = u2)	
	# 5
	Product.objects.using("testing").create(name = "Suit", 
		price = 40, in_stock = True, owner = u1)	
	# 6
	Product.objects.using("testing").create(name = "Meat", 
		price = 78, in_stock = True, owner = u1)	







