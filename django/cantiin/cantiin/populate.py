from products.models import Product



def drop_db():
	from django.db import connection
	cursor = connection.cursor()
	cursor.execute(“DROP DATABASE %s;”, [connection.settings_dict['NAME']])

def create_db():
	from django.db import connection
	cursor = connection.cursor()
	cursor.execute(“CREATE DATABASE %s;”, [connection.settings_dict['NAME']])

def drop_create_db():
	drop_db()
	create_db()





