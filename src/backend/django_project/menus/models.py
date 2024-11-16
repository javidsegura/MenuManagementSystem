"""
A model is an entity in database. Here you provide the template for that entity that will be used 
through the Django interface
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from storages.backends.s3boto3 import S3Boto3Storage

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

class Restaurant(models.Model):
    """
    __str_: defines the name of the object (each record)
    Meta Class: defines metadata about the model
        - verbose_name: name of the model in singular
        - verbose_name_plural: name of the model in plural
    """
    name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=3, null=True, blank=True)
    zip = models.SmallIntegerField(null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"

class MenuVersion(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    version_number = models.IntegerField(editable=False)
    composite_id = models.CharField(max_length=255, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only for new instances
            # Get the latest version number for this specific restaurant
            latest_version = MenuVersion.objects.filter(
                restaurant=self.restaurant
            ).order_by('-version_number').first()
            
            # Set the new version number
            self.version_number = (latest_version.version_number + 1) if latest_version else 1
            
            # Create a more unique composite_id using restaurant ID
            self.composite_id = f"{self.restaurant.id}:{self.restaurant.name}-v{self.version_number}"
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.composite_id
    
    class Meta:
        verbose_name = verbose_name_plural = "Menu Versions"

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    version = models.ForeignKey(MenuVersion, on_delete=models.CASCADE, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # should be readonly and given from the current logged in user automatically
    active_status = models.BooleanField(default=True, null=True, blank=True)
    available_until = models.DateField(null=True, blank=True)
    available_from = models.DateField(null=True, blank=True)
    timeUpload = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    menu_file = models.FileField(
                        null=True,
                        blank=True) # add storage=S3Boto3Storage() if using AWS S3

    def __str__(self):
        return f"{self.restaurant.name}:{self.id}" if self.restaurant else f"No restaurant: {self.id}"
    
    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"


class MenuSection(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=99, null=True, blank=True)

    def __str__(self):
        return f"{self.menu.restaurant.name}:{self.menu.id}:{self.name}"
    
    class Meta:
        verbose_name = "Menu Section"
        verbose_name_plural = "Menu Sections"


class MenuItem(models.Model):
    menu_section = models.ForeignKey(MenuSection, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=99, null=True, blank=True)
    description = models.CharField(max_length=99, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    currency = models.CharField(max_length=99, default='dollar', null=True, blank=True)
    available = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

class DietaryRestriction(models.Model):
    menu_items = models.ManyToManyField(MenuItem, related_name='dietary_restrictions') # relanted_name specified how to access the reverse relationship
    name = models.CharField(max_length=99, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Dietary Restriction"
        verbose_name_plural = "Dietary Restrictions"


class AuditLog(models.Model):

    menu_version = models.ForeignKey(MenuVersion, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=99, null=True, blank=True)
    phase = models.CharField(max_length=99, null=True, blank=True)
    time_registered = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    other = models.CharField(max_length=99, null=True, blank=True) # this could be a json

    def __str__(self):
        return f"{self.menu.restaurant.name}:{self.menu.id}"
    
    class Meta:
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"
    