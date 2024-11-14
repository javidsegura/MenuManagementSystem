from django.db import models
from django.contrib.auth.models import AbstractUser
from storages.backends.s3boto3 import S3Boto3Storage


# Create your models here. 
# All the databases entities will be here

"""
This module contains the entities included in datadefinition.sql for the menu app. 
Note slight differences may apply.
"""


class User(AbstractUser):
     # These fields are already included from AbstractUser:
    # username
    # password
    # first_name
    # last_name
    # email
    # is_staff
    # is_active
    # date_joined
    country = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=3, null=True, blank=True)
    zip = models.SmallIntegerField(null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self): 
        """ represnts the object namein the admin interface """
        return self.username

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now_add=True, null=True) # auto_now_add is a default value for current time

    def __str__(self):
        return f"{self.id}:{self.user.username}"

class Restaurant(models.Model):
    opening_hours = models.ManyToManyField('OpeningHours', related_name='restaurants')
    name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=3, null=True, blank=True)
    zip = models.SmallIntegerField(null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

class OpeningHours(models.Model):
    DAYS_OF_WEEK = [ # (actual_val, interface_val)
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK, null=True)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True) # time is 24 hour

    def __str__(self):
        return f"{self.day_of_week}: {self.open_time} - {self.close_time}"
    
class MenuVersion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    time_upload = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.restaurant.name}:{self.id}"

class Menu(models.Model):
    menu_version = models.ForeignKey(MenuVersion, on_delete=models.CASCADE)
    active_status = models.BooleanField(default=True, null=True, blank=True)
    available_until = models.DateField(null=True, blank=True)
    available_from = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=3, null=True, blank=True)
    zip = models.SmallIntegerField(null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    menu_file = models.FileField(storage=S3Boto3Storage(),
                                  upload_to='menu_files/', null=True, blank=True)

    def __str__(self):
        return f"{self.menu_version.restaurant.name}:{self.menu_version.id}"

class MenuSection(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=99, null=True, blank=True)

    def __str__(self):
        return f"{self.menu.menu_version.restaurant.name}:{self.menu.id}:{self.name}"


class MenuItem(models.Model):
    menu_section = models.ForeignKey(MenuSection, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=99, null=True, blank=True)
    description = models.CharField(max_length=99, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    currency = models.CharField(max_length=99, default='dollar', null=True, blank=True)
    available = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.name

class DietaryRestriction(models.Model):
    menu_items = models.ManyToManyField(MenuItem, related_name='dietary_restrictions') # relanted_name specified how to access the reverse relationship
    description = models.CharField(max_length=99, null=True, blank=True)

    def __str__(self):
        return self.description

class AuditLog(models.Model):
    STATUS_CHOICES = [
        ('received', 'Received'),
        ('processed', 'Processed'),
        ('uploaded', 'Uploaded'),
    ]
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, null=True, blank=True)
    action = models.CharField(max_length=99, null=True, blank=True)
    entity_affected = models.CharField(max_length=99, null=True, blank=True)
    old_value = models.CharField(max_length=99, null=True, blank=True)
    new_value = models.CharField(max_length=99, null=True, blank=True)

    def __str__(self):
        return f"{self.menu.menu_version.restaurant.name}:{self.menu.id}"
    