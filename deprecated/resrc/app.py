TESTING=True
"""
TESTING=False 	IN CASE OF PRODUCTION
TESTING=True 	IN CASE OF TESTING
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets
import os
from __init__ import db, SECRET
from models import (NotReceived, User, Product, Order, #Image,
	db_drop_and_create_all, populate_tables)
from auth import (requires_auth)
from flask_cors import CORS
from pydantic_models import (validate_model_id, validate_model_id_pydantic,
UserPost, UserUpdatePassword, ProductPost, OrderPost, OrderUpdate)
from flask_pydantic import validate


if "SECRET" in os.environ:
	SECRET = os.environ["SECRET"]




class config:
	#SECRET_KEY=os.urandom(32)
	SECRET_KEY=secrets.token_urlsafe(5000)
	basedir = os.path.abspath(os.path.dirname(__file__))
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = "sqlite:///databases/database.sqlite"
	SQLALCHEMY_TRACK_MODIFICATIONS= False


class config_test:
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = "sqlite:///databases/test.sqlite"

class config_docker:
	SQLALCHEMY_DATABASE_URI = "sqlite:////database//database.sqlite"


def create_app(DOCKER=False,testing=TESTING):
	app = Flask(__name__)
	app.config.from_object(config)
	if TESTING:
		app.config.from_object(config_test)
	if DOCKER:
		app.config.from_object(config_docker)

	db.app = app
	db.init_app(app)
	db.create_all()

	CORS(app,resources={r"*":{"origins":"*"}})
	@app.after_request
	def after_request(response):
		response.headers.add("Access-Control-allow-Origin","*")
		response.headers.add("Access-Control-allow-Headers",
			"Content-Type,Autorization,true")
		response.headers.add("Access-Control-allow-Methods",
			"GET,PUT,POST,DELETE,OPTIONS")
		db.session.rollback()
		return response













































	@app.route('/r', methods=['GET'])
	def raised():
		# Testng the ability to raise custom responses
		abort(make_response(jsonify({"sucess":True}),200))
		return jsonify({"success":False})


	@app.route('/', methods=['GET'])
	def home():
		return render_template('pages/index.html')

	@app.route('/add-product', methods=['GET'])
	def add_product():
		return render_template('pages/add_product.html')

	@app.route('/add-image', methods=['GET'])
	def add_image():
		return render_template('pages/add_image.html')

	@app.route('/cart', methods=['GET'])
	def cart():
		return render_template('pages/cart.html')

	@app.route('/edit-product', methods=['GET'])
	def edit_product():
		return render_template('pages/edit_product.html')

	@app.route('/login', methods=['GET'])
	def login():
		return render_template('pages/login.html')

	@app.route('/manage-products', methods=['GET'])
	def manage_products():
		return render_template('pages/manage_products.html')

	@app.route('/manage-images', methods=['GET'])
	def manage_images():
		return render_template('pages/manage_images.html')

	@app.route('/product', methods=['GET'])
	def product():
		return render_template('pages/product.html')

	@app.route('/signup', methods=['GET'])
	def signup():
		return render_template('pages/signup.html')

	@app.route('/about', methods=['GET'])
	def about():
		return render_template('pages/about.html')

	@app.route('/test', methods=['GET'])
	def test_template():
		return render_template('pages/test.html')











	"""
	1)	"/clear_tables"-------->"GET" , "OPTIONS"
	"""
	@app.route("/clear_tables", methods=["GET"])
	def clear_all_tables():
		test_only()
		db_drop_and_create_all()
		"""
Tests: test_02_populate_test
		"""
		return jsonify({"success":True})








	"""
	2)	"/populate" ->--------->"GET" , "OPTIONS"
	"""
	@app.route("/populate", methods=["GET"])
	def populate_all_tables():
		test_only()
		#This endpoint will clear all the data in the database and
		#populate with new data
		try:
			populate_tables()
			return jsonify({"success":True})
		except:
			abort(422) #Unprocessible
		"""
Tests: test_01_clear_tables
		"""



	"""
	User endpoints:
	post_users
	delete users
	login
	"""


	@app.route("/users/who", methods=["POST"])
	def users_who():
		#This endpoint will tell if the user should pass or not
		#and if his token expired, it will refresh it
		if "cantiin" not in request.cookies:
			abort(401)
		#Now the cookie exists
		token = request.cookies["cantiin"]
		#print(SECRET,flush=True)
		#print(request.cookies,flush=True)
		token_validation = validate_token(
			token=token,secret=SECRET)
		#print(token_validation,flush=True)
		#print("WHO: "+str(token_validation),flush=True)
		if token_validation["case"]==3:
			abort(401)
		if token_validation["case"]==2:
			res=jsonify({"success":True})
			user_id=token_validation["payload"]["uid"]
			res.set_cookie
			response=auth_cookie_response(
				response={"success":True,
				"result":"refreshed expired token",
				"user_id":user_id},
				user_id=user_id)
			return response
		else:
			return jsonify({"success":True,
				"result":"user is logged in",
				"user_id":token_validation["payload"]["uid"]})







	@app.route("/users", methods=["POST"])
	def post_users():
	#This endpoint will add a new user
		try:
			body = request.get_json()
		except:
			return my_error(status=400,
				description="request body can not be parsed to json")
		try:
			username = body.get("username",None)
			password1 = body.get("password1",None)
			password2 = body.get("password2",None)
		except:
			return my_error(status=400,
				description = "there is no request body")

		#Validating inputs one by one
		username_validation = validate_must(
			input=username,type="s",input_name_string="username",
			minimum=2,maximum=150)
		password1_validation = validate_must(
			input=password1,type="s",input_name_string="password1",
			minimum=8,maximum=150)
		password2_validation = validate_must(
			input=password2,type="s",input_name_string="password2",
			minimum=8,maximum=150)

		#Validating inputs a group
		val_group=validate_must_group(
			[username_validation,password1_validation
			,password2_validation])

		#Now we will validate all inputs as a group
		if val_group["case"] == True:
			# Success: they pass the conditions
			username,password1,password2=val_group["result"]
		else:
			# Failure: Something went wrong
			return val_group["result"]
		#Now we have username, password1 and password2 as strings

		#validate that the username has no white spaces
		if " " in username:
			return my_error(status=422,
				description="username can not contain white spaces")

		#Validate that this username is unique
		all_users=User.query.all()
		all_names=[str(u.username) for u in all_users]
		if username in all_names:
			return my_error(status=422,
				description="this username already exists")

		#Validate that these passwords are not the same
		if password1!=password2:
			return my_error(status=422,
				description="please enter the same password")

		#Create the user
		new_user = User(username=username, password=password1)

		#Insert the user in the database
		try:
			new_user.insert()
			response=auth_cookie_response(
				response={"success":True,"user":new_user.simple()},
				user_id=new_user.id)
			return response
		except Exception as e:
			raise(e)
			db.session.rollback()
			abort(500)






	@app.route("/users", methods=["DELETE"])
	@requires_auth()
	def delete_users(payload):
	#This endpoint will delete an existing user
		user_id=payload["uid"]
		users_query=User.query
		user_id_validation=validate_model_id(
			input_id=user_id,model_query=users_query
			,model_name_string="user")
		if user_id_validation["case"]==1:
			#The user exists
			user=user_id_validation["result"]

		else:
			#No user with this id, can not convert to int,
			# or id is missing (Impossible)
			return my_error(
				status=user_id_validation["result"]["status"],
				description=user_id_validation
				["result"]["description"])

		#Now, we have "user", this is essential

		try:
			# Finally, deleting the user itself
			user.delete()
			r=jsonify({"success":True,
					"result":"user deleted successfully"})
			cookies=request.cookies
			for co in cookies:
				r.set_cookie(co,value="",expires=-50)
			return r
			#return jsonify({"success":True,
			#	"result":"user deleted successfully"})
		except Exception as e:
			raise(e)
			db.session.rollback()
			abort(500)














	@app.route("/users/login", methods=["POST"])
	def login_users():
	#This endpoint will log the user in
		try:
			body = request.get_json()
		except:
			return my_error(status=400,
				description="request body can not be parsed to json")
		try:
			username = body.get("username",None)
			password = body.get("password",None)
		except:
			return my_error(status=400,
				description = "there is no request body")

		#Validating inputs one by one
		username_validation = validate_must(
			input=username,type="s",input_name_string="username",
			minimum=2,maximum=150)
		password_validation = validate_must(
			input=password,type="s",input_name_string="password",
			minimum=8,maximum=150)

		#Validating inputs a group
		val_group=validate_must_group(
			[username_validation,password_validation])

		#Now we will validate all inputs as a group
		if val_group["case"] == True:
			# Success: they pass the conditions
			username,password=val_group["result"]
		else:
			# Failure: Something went wrong
			return val_group["result"]
		#Now we have username, password and password2 as strings

		users=User.query.all()

		#Validate that this username and password are correct
		all_users=User.query.all()
		the_user_id="";

		for usr in all_users:
			if (str(usr.username) == str(username) and
				str(usr.password) == str(password)):
				the_user_id=usr.id # Here we go the user id
				break

		if the_user_id=="":
			return my_error(status=422,
				description="wrong username or password")
		#now we have the_user_id as integer


		response=auth_cookie_response(
			response={"success":True,
			"result":"logged in successfully",
			"user_id":the_user_id},
			user_id=the_user_id)
		return response

		#return jsonify()


	@app.route("/users/logout", methods=["POST"])
	def logout_users():
	#This endpoint will log the user out
		cookies = request.cookies
		r=jsonify({"success":True,
			"result":"logged out successfully"})
		for co in cookies:
			r.set_cookie(co,value="",expires=-50)
		return r
		#return jsonify({"success":True,
		#	"result":"logged out successfully"})











	@app.route("/users/login/test", methods=["POST"])
	def login_test():
		test_only()
	#This endpoint will log the user in
		response=auth_cookie_response(
			response={"success":True,
			"result":"logged in successfully",
			"user_id":1},
			user_id=1)
		return response


	@app.route("/users/login/expired", methods=["POST"])
	def login_expired():
		test_only()
	#This endpoint will log the user in with expired token
		res = jsonify(
					{"success":True,
					"result":"setting expired token successfully"})
		expired_token=generate_token(user_id=1,secret=SECRET,
    		expiration_delta=timedelta(days=-7),
    		issued_at=datetime.now())
		res.set_cookie('cantiin',
		 value=expired_token["result"],
			httponly=True, samesite='Lax')
		return res,200












	"""
	3)	and 4) Product endpoints
	"""
	@app.route("/products", methods=["GET"])
	def get_products():
		#print("Cookies: "+str(request.cookies),flush=True)
	#This endpoint will return all the products
		#recievng inputs:
		#in_stock has a fall back value of True (The default)
		in_stock = request.args.get('in_stock',True)

		#in stock now has one of two values
		#1) input value
		#2) True (Fall back value)
		#-	I can not be equal to None at all
		#-	Even if equal to None, it will be rejected
		in_stock_validation = validate_must(
			input=in_stock,type="b",input_name_string="in_stock")

		#Now we will validate the in_stock input
		if in_stock_validation["case"] == True:
			# Success: True or false
			in_stock=in_stock_validation["result"]
		else:
			# Failure: Can't convert to boolean or None (Impossible)
			return in_stock_validation["result"]

		#Now: There are 2 possibilties
			#1) in_stock = True
			#2) in_stock=False
			#input now must have been converted to True or False

		if in_stock == True:
			products = get_in_stock_products()
		else:
			products = Product.query.order_by(Product.id).all()

		to_return=[p.simple() for p in products]
		return jsonify({"success":True,"products":to_return})


	@app.route("/products", methods=["POST"])
	@requires_auth()
	def post_products(payload):
	#This endpoint will add a new product
		#print(payload,flush=True)
		try:
			body = request.get_json()
		except:
			return my_error(status=400,
				description="request body can not be parsed to json")
		try:
			name = body.get("name",None)
			price = body.get("price",None)
			in_stock = body.get("in_stock",None)
			#seller_id = body.get("seller_id",None)
		except:
			return my_error(status=400,
				description = "there is no request body")

		#Validating inputs one by one
		name_validation = validate_must(
			input=name,type="s",input_name_string="name",
			minimum=3,maximum=150)
		price_validation = validate_must(
			input=price,type="f",input_name_string="price",
			minimum=0.1,maximum=1000000)
		in_stock_validation = validate_must(
			input=in_stock,type="b",input_name_string="in_stock")
		#seller_id_validation = validate_must(
		#	input=seller_id,type="i",input_name_string="seller_id",
		#	minimum=1,maximum=100000000000000000)

		#Validating inputs a group
		val_group=validate_must_group(
			[name_validation,price_validation,
			in_stock_validation])

		#Now we will validate all inputs as a group
		if val_group["case"] == True:
			# Success: they pass the conditions
			name,price,in_stock=val_group["result"]
		else:
			# Failure: Something went wrong
			return val_group["result"]

		seller_id = payload["uid"]
		users_query=User.query
		user_id_validation=validate_model_id(
			input_id=seller_id,model_query=users_query
			,model_name_string="user")
		if user_id_validation["case"]==1:
			#The user exists
			seller=user_id_validation["result"]
		else:
			#No user with this id, can not convert to int,
			# or id is missing
			return my_error(
				status=user_id_validation["result"]["status"],
				description=user_id_validation
				["result"]["description"])
		seller_id = seller.id

		#Create the product
		new_product = Product(name=name, price=price,
			seller_id=seller_id, in_stock=in_stock)

		#Insert the product in the database
		try:
			new_product.insert()
			return jsonify(
				{"success":True,"product":new_product.simple()})
		except Exception as e:
			db.session.rollback()
			abort(500)





	@app.route("/products/<int:product_id>", methods=["PUT"])
	@requires_auth()
	def edit_products(payload,product_id):
	#This endpoint will add a new product
	#This is the correct arrangement
	#payload then product id
	#the opposite will result in error
		#print("product_id: "+str(product_id),flush=True)
		#print("payload: "+str(payload),flush=True)
		try:
			body = request.get_json()
		except:
			return my_error(status=400,
				description="request body can not be parsed to json")
		try:
			name = body.get("name",None)
			price = body.get("price",None)
			in_stock = body.get("in_stock",None)
		except:
			return my_error(status=400,
				description = "there is no request body")

		#There can not be 0 fields to change
		#There must be at least one input field
		if (name==None and price==None and in_stock==None):
			return my_error(status=400,
				description = "you must at least enter"
				" one field to change")

		products_query=Product.query

		product_id_validation=validate_model_id(
			input_id=product_id,model_query=products_query
			,model_name_string="product")
		if product_id_validation["case"]==1:
			#The product exists
			product=product_id_validation["result"]

		else:
			#No product with this id, can not convert to int,
			# or id is missing (Impossible)
			return my_error(
				status=product_id_validation["result"]["status"],
				description=product_id_validation
				["result"]["description"])

		#Now, we have "product", this is essential

		#there will be no None
		if name == None:name=product.name
		if price == None:price=product.price
		if in_stock == None:in_stock=product.in_stock
		#Now there is no None
		#There are default values
		#This step can not change it's place because
		#here we need default values

		name_validation = validate_must(
			input=name,type="s",input_name_string="name",
			minimum=3,maximum=150)
		price_validation = validate_must(
			input=price,type="f",input_name_string="price",
			minimum=0.1,maximum=1000000)
		in_stock_validation = validate_must(
			input=in_stock,type="b",input_name_string="in_stock")
		#seller_id_validation = validate_must(
		#	input=seller_id,type="i",input_name_string="seller_id",
		#	minimum=1,maximum=100000000000000000)
		#seller_id can not change

		val_group=validate_must_group(
			[name_validation,price_validation,
			in_stock_validation])

		#Now we will validate all inputs as a group
		if val_group["case"] == True:
			# Success: they pass the conditions
			name,price,in_stock,=val_group["result"]
		else:
			# Failure: Something went wrong
			return val_group["result"]

		#Making sure that this user can change this product
		if int(product.seller_id) != payload["uid"]:
			return my_error(
				status=403,
				description=
				"you can not change this product, because"+
				" you are not the one who created it")

		#Finally: applying changes
		product.name=name
		product.price=price
		product.in_stock=in_stock

		try:
			product.update()
			return jsonify(
				{"success":True,"product":product.simple()})
		except Exception as e:
			db.session.rollback()
			abort(500)




	@app.route("/products/<int:product_id>", methods=["DELETE"])
	@requires_auth()
	def delete_products(payload,product_id):
	#This endpoint will delete an existing product

		products_query=Product.query
		product_id_validation=validate_model_id(
			input_id=product_id,model_query=products_query
			,model_name_string="product")
		if product_id_validation["case"]==1:
			#The product exists
			product=product_id_validation["result"]

		else:
			#No product with this id, can not convert to int,
			# or id is missing (Impossible)
			return my_error(
				status=product_id_validation["result"]["status"],
				description=product_id_validation
				["result"]["description"])

		#Now, we have "product", this is essential

		#Making sure that this user can delete this product
		if int(product.seller_id) != payload["uid"]:
			return my_error(
				status=403,
				description=
				"you can not delete this product, because"+
				" you are not the one who created it")

		try:
			# Finally, deleting the product itself
			product.delete()
			return jsonify(
				{"success":True,
				"result":"product deleted successfully"})
		except Exception as e:
			db.session.rollback()
			abort(500)


	@app.route("/products/users", methods=["GET"])
	@requires_auth()
	def get_products_users(payload):
		user_id=int(payload["uid"])
		products = Product.query.filter(
			Product.seller_id==user_id).order_by(
			Product.id).all()
		to_return=[p.simple() for p in products]
		return jsonify({"success":True,"products":to_return})







































	"""
	5) and 6) Order endpoints
	"""
	@app.route("/orders", methods=["GET"])
	@requires_auth()
	def get_orders(payload):
	#This endpoint will return all the orders

		user_id=payload["uid"]

		"""user_id_validation = validate_must(
			input=user_id,type="i",input_name_string="user_id",
			minimum=1,maximum=1000000000000000000000)

		#Now we will validate the user_id input
		if user_id_validation["case"] == True:
			# Success: value is integer
			user_id=user_id_validation["result"]
		else:
			# Failure: Can't convert to integer or None
			return user_id_validation["result"]

		#Now: There is only one possibility
			#1) type(user_id) = int
			#input now must have been converted to integer"""


		#Filtering by user_id
		orders = Order.query.filter(
			Order.user_id==user_id).order_by("id").all()

		to_return=[o.get_dict() for o in orders]
		return jsonify({"success":True,"orders":to_return})



	@app.route("/orders", methods=["POST"])
	@requires_auth()
	def post_orders(payload):
	#This endpoint will add a new product
		try:
			body = request.get_json()
		except:
			return my_error(status=400,
				description="request body can not be parsed to json")
		try:
			#user_id = body.get("user_id",None)
			product_id = body.get("product_id",None)
			amount = body.get("amount",None)
		except:
			return my_error(status=400,
				description = "there is no request body")

		#Validating inputs one by one
		#user_id_validation = validate_must(
		#	input=user_id,type="i",input_name_string="user_id",
		#	minimum=0,maximum=1000)
		amount_validation = validate_must(
			input=amount,type="i",input_name_string="amount",
			minimum=1,maximum=1000000000)

		#Validating inputs a group
		val_group=validate_must_group(
			[amount_validation])

		#Now we will validate all inputs as a group
		if val_group["case"] == True:
			# Success: they pass the conditions
			amount=val_group["result"][0]
		else:
			# Failure: Something went wrong
			return val_group["result"]
		#Now the inputs user_id and amount are validated

		#Now we will validate product_id
		products_query=Product.query
		product_id_validation=validate_model_id(
			input_id=product_id,model_query=products_query
			,model_name_string="product")
		if product_id_validation["case"]==1:
			#The product exists
			product=product_id_validation["result"]
		else:
			#No product with this id, can not convert to int,
			# or id is missing
			return my_error(
				status=product_id_validation["result"]["status"],
				description=product_id_validation
				["result"]["description"])

		product_id = product.id
		#Now, we have "product_id", this is essential

		user_id=payload["uid"]

		#Create the Order
		new_order = Order(user_id=user_id, amount=amount,
			product_id=product_id)
		#Insert the order in the database
		try:
			new_order.insert()
			return jsonify(
				{"success":True,"order":new_order.get_dict()})
		except Exception as e:
			db.session.rollback()
			abort(500)





	@app.route("/orders/<int:order_id>", methods=["PUT"])
	@requires_auth()
	def edit_orders(payload,order_id):
	#This endpoint will edit an exiting order
		try:
			body = request.get_json()
		except:
			return my_error(status=400,
				description="request body can not be parsed to json")
		try:
			amount = body.get("amount",None)
		except:
			return my_error(status=400,
				description = "there is no request body")

		#There can not be 0 fields to change
		#There must be at least one input field
		if (amount==None):
			return my_error(status=400,
				description = "you must at least enter"
				" one field to change")

		#Validating inputs one by one
		amount_validation = validate_must(
			input=amount,type="i",input_name_string="amount",
			minimum=0,maximum=1000000000)

		#Now we will validate all inputs as a group
		if amount_validation["case"] == True:
			# Success: they pass the conditions
			amount=amount_validation["result"]
		else:
			# Failure: Something went wrong
			return amount_validation["result"]
		#Now the inputs user_id and amount are validated

		orders_query=Order.query

		order_id_validation=validate_model_id(
			input_id=order_id,model_query=orders_query
			,model_name_string="order")
		if order_id_validation["case"]==1:
			#The order exists
			order=order_id_validation["result"]

		else:
			#No order with this id, can not convert to int,
			# or id is missing (Impossible)
			return my_error(
				status=order_id_validation["result"]["status"],
				description=order_id_validation
				["result"]["description"])
		#Now, we have "order", this is essential

		#Now we validate if the this user can edit the order
		if int(order.user_id) != payload["uid"]:
			return my_error(
				status=403,
				description=
				"you can not edit this order, because"+
				" you are not the one who created it")


		#Finally: applying changes
		order.amount=amount

		if amount == 0:
			try:
				order.update()
				return jsonify(
					{"success":True,"result":"order"+
					" deleted successfully"})
			except Exception as e:
				db.session.rollback()
				abort(500)
		try:
			order.update()
			return jsonify(
				{"success":True,"order":order.get_dict()})
		except Exception as e:
			db.session.rollback()
			abort(500)




	@app.route("/orders/<int:order_id>", methods=["DELETE"])
	@requires_auth()
	def delete_orders(payload,order_id):
	#This endpoint will delete an existing order

		orders_query=Order.query
		order_id_validation=validate_model_id(
			input_id=order_id,model_query=orders_query
			,model_name_string="order")
		if order_id_validation["case"]==1:
			#The order exists
			order=order_id_validation["result"]
		else:
			#No order with this id, can not convert to int,
			# or id is missing (Impossible)
			return my_error(
				status=order_id_validation["result"]["status"],
				description=order_id_validation
				["result"]["description"])

		#Now, we have "order", this is essential

		#Now we validate if the this user can delete the order
		if int(order.user_id) != payload["uid"]:
			return my_error(
				status=403,
				description=
				"you can not delete this order, because"+
				" you are not the one who created it")

		try:
			# Finally, deleting the order itself
			order.delete()
			return jsonify(
				{"success":True,
				"result":"order deleted successfully"})
		except Exception as e:
			db.session.rollback()
			abort(500)















































































	@app.errorhandler(400)
	def bad_request(error):
		return jsonify({"success":False,"error":400,
			"message":"bad request"}),400


	@app.errorhandler(401)
	def unauthorized(error):
		return jsonify({"success":False,"error":401,
			"message":"unauthorized"}),401


	@app.errorhandler(403)
	def forbidden(error):
		return jsonify({"success":False,"error":403,
			"message":"forbidden"}),403


	@app.errorhandler(404)
	def not_found(error):
		return jsonify({"success":False,"error":404,
			"message":"not found"}),404


	@app.errorhandler(405)
	def method_not_allowed(error):
		return jsonify({"success":False,"error":405,
			"message":"method not allowed"}),405


	@app.errorhandler(422)
	def unprocessible(error):
		return jsonify({"success":False,"error":422,
			"message":"unprocessible"}),422


	@app.errorhandler(500)
	def internal_server_error(error):
		return jsonify({"success":False,"error":500,
			"message":"internal server error"}),500



	def test_only():
		if testing == False:
			abort(404)


	return app

if __name__ == '__main__':
	create_app().run()
