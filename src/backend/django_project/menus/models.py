from django.db import models
from django.contrib.auth.models import AbstractUser

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
    upload_time = models.DateTimeField(auto_now_add=True, null=False) # auto_now_add is a default value for current time

    def __str__(self):
        return self.user.username

class Restaurant(models.Model):
    name = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=50, null=False)
    country = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=50, null=False)
    state = models.CharField(max_length=3, null=False)
    zip = models.SmallIntegerField(null=False)
    street = models.CharField(max_length=50, null=False)
    opening_hours = models.ManyToManyField('OpeningHours', related_name='restaurants')

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
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK, null=False)
    open_time = models.TimeField(null=False)
    close_time = models.TimeField(null=False) # time is 24 hour

    def __str__(self):
        return self.day_of_week
    
class MenuVersion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    time_upload = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.user.username

class Menu(models.Model):
    section = models.CharField(max_length=50, null=False) # I am not sure if this should be an independent entity
    menu_version = models.ForeignKey(MenuVersion, on_delete=models.CASCADE)
    active_status = models.BooleanField(default=True, null=False)
    available_until = models.DateField(null=False)
    available_from = models.DateField(null=False)
    country = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=50, null=False)
    state = models.CharField(max_length=3, null=False)
    zip = models.SmallIntegerField(null=False)
    street = models.CharField(max_length=50, null=False)
    menuPdf = models.FileField(upload_to='menu_pdfs/', null=True, blank=True)

    def __str__(self):
        return self.section

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=99, null=False)
    description = models.CharField(max_length=99, null=False)
    price = models.IntegerField(null=False)
    currency = models.CharField(max_length=99, default='dollar', null=False)
    available = models.BooleanField(null=False)

    def __str__(self):
        return self.name

class DietaryRestriction(models.Model):
    description = models.CharField(max_length=99, null=False)
    menu_items = models.ManyToManyField(MenuItem, related_name='dietary_restrictions') # relanted_name specified how to access the reverse relationship

    def __str__(self):
        return self.description

class AuditLog(models.Model):
    STATUS_CHOICES = [
        ('received', 'Received'),
        ('processed', 'Processed'),
        ('uploaded', 'Uploaded'),
    ]
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=False)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, null=False)
    action = models.CharField(max_length=99, null=False)
    entity_affected = models.CharField(max_length=99, null=False)
    old_value = models.CharField(max_length=99, null=True, blank=True)
    new_value = models.CharField(max_length=99, null=True, blank=True)

    def __str__(self):
        return self.menu.section
    