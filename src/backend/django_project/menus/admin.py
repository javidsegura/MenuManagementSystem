""" Specify the models you want to display in the admin interface 


Notes on some functions:
1. format_html: used to format the html of the admin interface
2. list_display: represents the columns in the admin interface
3. list_filter: filter based upon the fields
4. readonly_fields: fields that are readonly

"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html  
from .models import (
    User,
    Post,
    MenuVersion,
    Restaurant,
    OpeningHours,
    Menu,
    MenuItem,
    DietaryRestriction,
    AuditLog,
    MenuSection
)

import base64
from openai import OpenAI
import os
from menus.utils.ai_call import ai_call
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff') 
    list_filter = ('is_staff', 'is_superuser') 
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('country', 'city', 'state', 'zip', 'street')}),
    )

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'state', 'phone', 'email')
    search_fields = ('name', 'city')

@admin.register(OpeningHours)
class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ('id', 'day_of_week', 'open_time', 'close_time')
    list_filter = ('day_of_week',)

@admin.register(MenuVersion)
class MenuVersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restaurant', 'time_upload')
    list_filter = ('time_upload', 'restaurant')

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """
    Modify the save_model function to call processing functions before.
    Menu is the whole record of the model.
        -  menu.menu_file is uploaded file. It has the following attributes:
            - url: the link to the file in the server
            - name: the name of the file
            - path: the path to the file in the server
            - size: the size of the file
            - file: the actual file object
    
    """
    list_display = ('id', 'menu_version', 'active_status', 'available_from', 'available_until', 'menu_file_link')
    list_filter = ('active_status', 'available_from', 'available_until')
    
    def save_model(self, request, menu, form, change):
        """First execute this body then save model as usual"""
        print(f"Saving model {menu.id}")
        if menu.menu_file and not change:  # Only process on new uploads
            try:
                ai_call(menu.menu_file)
            except Exception as e:
                self.message_user(request, f"Error processing menu: {str(e)}", level='ERROR')

        super().save_model(request, menu, form, change)

    def menu_file_link(self, menu): # referred in list_display
        if menu.menu_file:
            return format_html('<a href="{}" target="_blank">View File</a>', menu.menu_file.url)
        return '-'

    menu_file_link.short_description = 'Menu File' # Change the column name in the admin interface

@admin.register(MenuSection)
class MenuSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'menu')
    list_filter = ('menu',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'menu_section', 'price', 'currency', 'available')
    list_filter = ('available', 'currency', 'menu_section')
    search_fields = ('name', 'description')

@admin.register(DietaryRestriction)
class DietaryRestrictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'upload_time')
    list_filter = ('upload_time',)

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'menu', 'status', 'action', 'entity_affected')
    list_filter = ('status',)
    #readonly_fields = ('menu', 'status', 'action', 'entity_affected', 'old_value', 'new_value')

