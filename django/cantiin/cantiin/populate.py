from users.models import User
from groups.models import Group
from group_members.models import GroupMember
from django.test import Client


"""
Deleting
"""



def delete_users():
	User.objects.all().delete()

"""def delete_groups():
	Group.objects.all().delete()

def delete_group_members():
	GroupMember.objects.all().delete()
"""

def delete_all_records():
	delete_group_members()
	#delete_groups()
	#elete_users()



"""
Populating
"""

def poplating_user_using_djoser():
	c = Client()
	data = {"username":"123",
	"password":"elephant_crusher"}
	response = c.post('/auth/users/', data=data)
	# print(response.status_code)
	# 201
	# print(response.data)
	# {'email': '', 'username': '123', 'id': 315}
	#print(response.__dict__)
"""
{
	'template_name': None, 
	'context_data': None, 
	'using': None, 
	'_post_render_callbacks': [], 
	'_request': None, 
	'_headers': {'content-type': 
	('Content-Type', 'application/json'), 
	'vary': ('Vary', 'Accept, Cookie'), 
	'allow': ('Allow', 'GET, POST, HEAD, OPTIONS'), 
	'x-frame-options': ('X-Frame-Options', 'DENY'), 
	'content-length': ('Content-Length', '38'), 
	'x-content-type-options': ('X-Content-Type-Options', 
	'nosniff'), 
	'referrer-policy': ('Referrer-Policy', 
	'same-origin')}, 
	'_resource_closers': [], 
	'_handler_class': None, 
	'cookies': <SimpleCookie: >, 
	'closed': True, 'status_code': 201, 
	'_reason_phrase': None, '_charset': None, 
	'_container': [b'{"email":"","username":"123",
	"id":731}'], 
	'_is_rendered': True, 
	'data': {'email': '', 'username': '123', 'id': 731}, 
	'exception': False, 
	'content_type': None, 
	'accepted_renderer': <rest_framework.renderers.
	JSONRenderer object at 0x000001C29EFFF2C8>, 
	'accepted_media_type': 'application/json', 
	'renderer_context': {'view': <djoser.views.UserViewSet 
	object at 0x000001C29EFF4F88>, 
	'args': (), 
	'kwargs': {}, 
	'request': <rest_framework.request.Request: 
	POST '/auth/users/'>, 
	'response': <Response status_code=201, 
	"application/json">}, 
	'wsgi_request': <WSGIRequest: POST '/auth/users/'>, 
	'exc_info': None, 
	'client': <django.test.client.Client object 
	at 0x000001C29EFE0688>, 
	'request': 
	{
		'PATH_INFO': '/auth/users/', 
		'REQUEST_METHOD': 'POST', 
		'SERVER_PORT': '80', 
		'wsgi.url_scheme': 'http', 
		'CONTENT_LENGTH': '181', 
		'CONTENT_TYPE': 
		'multipart/form-data; 
		boundary=BoUnDaRyStRiNg', 
		'wsgi.input': <django.test.client.
		FakePayload object at 0x000001C29EFE0248>, 
		'QUERY_STRING': ''
	}, 
	'templates': [], 
	'context': None, 
	'json': functools.partial(<bound method ClientMixin._
	parse_json of <django.test.client.Client object 
	at 0x000001C29EFE0688>>, 
	<Response status_code=201, "application/json">), 
	'resolver_match': <SimpleLazyObject: 
	<function Client.request.<locals>.<lambda> at 
	0x000001C29F03A1F8>>
}
"""

def create_djoser_user(username:str,password:str):
	c = Client()
	data = {"username":username,
	"password":password}
	response = c.post('/auth/users/', data=data)




def create_djoser_users(users_list):
	for u in users_list:
		create_djoser_user(u["username"],u["password"])


def populate_users_easy(users_list):
	for u in users_list:
		User.objects.create(username = u["username"],
			email = "",password = u["password"]) # 1



users_list_test = [
	{"username":"user_01","password":"uncommon_01"},
	{"username":"user_02","password":"uncommon_02"},
	{"username":"user_03","password":"uncommon_03"},
	{"username":"user_04","password":"uncommon_04"},
	{"username":"user_05","password":"uncommon_05"},
	{"username":"user_06","password":"uncommon_06"},
	{"username":"user_07","password":"uncommon_07"},
	{"username":"user_08","password":"uncommon_08"},
	{"username":"user_09","password":"uncommon_09"},
	{"username":"user_10","password":"uncommon_10"},
	{"username":"user_11","password":"uncommon_11"},
	{"username":"user_12","password":"uncommon_12"},
	{"username":"user_13","password":"uncommon_13"},
	{"username":"user_14","password":"uncommon_14"},
	{"username":"user_15","password":"uncommon_15"},
	{"username":"user_16","password":"uncommon_16"},
	{"username":"user_17","password":"uncommon_17"},
	{"username":"user_18","password":"uncommon_18"},
	{"username":"user_19","password":"uncommon_19"},
	{"username":"user_20","password":"uncommon_20"},
]




def populate_users(easy = True):
	delete_users()
	if easy:
		populate_users_easy(users_list_test)
	else:
		create_djoser_users(users_list_test)






"""

def populate_groups():
	delete_groups()
	# 1
	Group.objects.create(
		name = "Eminem Fans", public=True)	
	# 2
	Group.objects.create(
		name = "Cooking Mania", public=True)	
	# 3
	Group.objects.create(
		name = "Social Issues", public=False)	




def populate_group_members():
	delete_group_members()
	users = User.objects.all() # 0:19
	groups = Group.objects.all() # 0:2
	
	# 1
	GroupMember.objects.create(
		member = users[0], 
		custom_group = groups[0], role="ADMIN")	
	# 2
	GroupMember.objects.create(
		member = users[1], 
		custom_group = groups[0], role="ADMIN")	
	# 3
	GroupMember.objects.create(
		member = users[2], 
		custom_group = groups[1], role="ADMIN")	
	# 4
	GroupMember.objects.create(
		member = users[0], 
		custom_group = groups[2], role="ADMIN")	
	# 5
	GroupMember.objects.create(
		member = users[3], 
		custom_group = groups[1], role="MODERATOR")	
	# 6
	GroupMember.objects.create(
		member = users[3], 
		custom_group = groups[0], role="MODERATOR")	
	# 7
	GroupMember.objects.create(
		member = users[4], 
		custom_group = groups[2], role="MODERATOR")	
	# 8
	GroupMember.objects.create(
		member = users[5], 
		custom_group = groups[0], role="MEMBER")	
	# 9
	GroupMember.objects.create(
		member = users[7], 
		custom_group = groups[0], role="MEMBER")	
	# 10
	GroupMember.objects.create(
		member = users[8], 
		custom_group = groups[0], role="MEMBER")	
	# 11
	GroupMember.objects.create(
		member = users[9], 
		custom_group = groups[0], role="MEMBER")	
	# 12
	GroupMember.objects.create(
		member = users[6], 
		custom_group = groups[1], role="MEMBER")	
	# 13
	GroupMember.objects.create(
		member = users[7], 
		custom_group = groups[1], role="MEMBER")	
	# 14
	GroupMember.objects.create(
		member = users[8], 
		custom_group = groups[1], role="MEMBER")	
	# 15
	GroupMember.objects.create(
		member = users[9], 
		custom_group = groups[1], role="MEMBER")	
	# 16
	GroupMember.objects.create(
		member = users[6], 
		custom_group = groups[2], role="MEMBER")	
	# 17
	GroupMember.objects.create(
		member = users[7], 
		custom_group = groups[2], role="MEMBER")	
	# 18
	GroupMember.objects.create(
		member = users[8], 
		custom_group = groups[2], role="MEMBER")	
	# 19
	GroupMember.objects.create(
		member = users[11], 
		custom_group = groups[0], role="MEMBER")	
	

"""





















def populate_all(easy=True):
	delete_all_records()
	populate_users(easy)
	#populate_groups()
	#populate_group_members()





def get_djoser_token(username:str,password:str):
	c = Client()
	data = {"username":username,
	"password":password}
	response = c.post("/auth/token/login", data=data)
	#print(response.__dict__)
	return response.data["auth_token"]
"""
{
'template_name': None, 
'context_data': None, 
'using': None, 
'_post_render_callbacks': [], 
'_request': None, 
'_headers': 
{
	'content-type': ('Content-Type', 'application/json'), 
	'vary': ('Vary', 'Accept'), 
	'allow': ('Allow', 'POST, OPTIONS'), 
	'x-frame-options': ('X-Frame-Options', 'DENY'), 
	'content-length': ('Content-Length', '57'), 
	'x-content-type-options': 
		('X-Content-Type-Options', 'nosniff'), 
		'referrer-policy': ('Referrer-Policy', 'same-origin')
}, 
'_resource_closers': [], 
'_handler_class': None, 
'cookies': <SimpleCookie: >, 
'closed': True, 
'status_code': 200, 
'_reason_phrase': None, 
'_charset': None, 
'_container': 
[b'{"auth_token":"2657df13c2352c96fdbe2e76e7cfda3f25df9865"}'], 
'_is_rendered': True, 


'data': {
	'auth_token': '2657df13c2352c96fdbe2e76e7cfda3f25df9865'
}, 
'exception': False, 
'content_type': None, 
'accepted_renderer': <rest_framework.renderers.JSONRenderer 
object at 0x0000011E4E60F748>, 
'accepted_media_type': 'application/json', 
'renderer_context': 
{
	'view': <djoser.views.TokenCreateView object at 0x0000011E4E60
	4C08>, 
	'args': (), 
	'kwargs': {}, 
	'request': <rest_framework.request.Request: POST '
	/auth/token/login/'>, 
	'response': <Response status_code=200, "application/json">
}, 
'wsgi_request': <WSGIRequest: POST '/auth/token/login/'>, 
'exc_info': None, 'client': <django.test.client.Client o
bject at 0x0000011E4E4328C8>, 
'request': 
{
	'PATH_INFO': '/auth/token/login/', 
	'REQUEST_METHOD': 'POST', 
	'SERVER_PORT': '80', 
	'wsgi.url_scheme': 'http', 
	'CONTENT_LENGTH': '180', 
	'CONTENT_TYPE': 'multipart/form-data; boundary=BoUnDaRyStRiNg', 
	'wsgi.input': <django.test.client.FakePayload object 
	at 0x0000011E4E604BC8>, 
	'QUERY_STRING': ''
}, 
'templates': [], 
'context': None, 
'json': functools.partial(<bound method ClientMixin._parse
	_json of <django.test.client.Client object at 
	0x0000011E4E4328C8>>, <Response status_code=200, 
	"application/json">), 
'resolver_match': <SimpleLazyObject: <function Client.reques
	t.<locals>.<lambda> at 0x0000011E4E8669D8>>
}
"""


