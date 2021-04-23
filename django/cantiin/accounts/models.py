from django.db import models

# Create your models here.

"""

"""

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	def __str__(self):
		return self.username






from rest_framework import serializers

class FullUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields="__all__"


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["id","username",
		"first_name","last_name","email","groups","password"]
		extra_kwargs = {'password': {'write_only': True}}




"""
python manage.py shell
from users.models import FullUserSerializer
serializer = FullUserSerializer()
print(repr(serializer))

exit()


# Full user Model
FullUserSerializer():
	id = IntegerField(label='ID', read_only=True)
	password = CharField(max_length=128)
	last_login = DateTimeField(allow_null=True, required=False)
	is_superuser = BooleanField(help_text='Designates that this user has all permissions without explicitly assi
gning them.', label='Superuser status', required=False)
	username = CharField(help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max
_length=150, validators=[<django.contrib.auth.validators.UnicodeUsernameValidator object>, <UniqueValidator(quer
yset=User.objects.all())>])
	first_name = CharField(allow_blank=True, max_length=150, required=False)
	last_name = CharField(allow_blank=True, max_length=150, required=False)
	email = EmailField(allow_blank=True, label='Email address', max_length=254, required=False)
	is_staff = BooleanField(help_text='Designates whether the user can log into this admin site.', label='Staff
status', required=False)
	is_active = BooleanField(help_text='Designates whether this user should be treated as active. Unselect this
instead of deleting accounts.', label='Active', required=False)
	date_joined = DateTimeField(required=False)
	groups = PrimaryKeyRelatedField(help_text='The groups this user belongs to. A user will get all permissions
granted to each of their groups.', many=True, queryset=Group.objects.all(), required=False)
	user_permissions = PrimaryKeyRelatedField(help_text='Specific permissions for this user.', many=True, querys
et=Permission.objects.all(), required=False)


"""



"""
python manage.py shell
from users.models import UserSerializer
serializer = UserSerializer()
print(repr(serializer))


exit()




UserSerializer():
	id = IntegerField(label='ID', read_only=True)
	username = CharField(help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, validators=[<django.contrib.auth.validators.UnicodeUsernameValidator object>, <UniqueValidator(queryset=User.objects.all())>])
	first_name = CharField(allow_blank=True, max_length=150, required=False)
	last_name = CharField(allow_blank=True, max_length=150, required=False)
	email = EmailField(allow_blank=True, label='Email address', max_length=254, required=False)
	groups = PrimaryKeyRelatedField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', many=True, queryset=Group.objects.all(), required=False)



"""