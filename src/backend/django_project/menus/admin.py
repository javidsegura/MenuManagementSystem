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
    Restaurant,
    Menu,
    MenuItem,
    DietaryRestriction,
    AuditLog,
    MenuSection, 
    MenuVersion
)

from menus.utils.extraction import ai_call
from menus.utils.insertion import populate_menu_data



@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff') 
    list_filter = ('is_staff', 'is_superuser') 
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('country', 'city', 'state', 'zip', 'street')}),
    )

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'state', 'phone', 'email', 
                    'website', 'country', 'zip', 'street')
    search_fields = ('name', 'city')

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
    list_display = ('id', 'restaurant', 'user_id', 'version', 'menu_file_link',
                    'active_status', 'available_from', 'available_until',
                    'timeUpload')
    list_filter = ('active_status', 'available_from', 'available_until')
    readonly_fields = ('user_id', 'version', "restaurant") # restaurante will be readonly, with default temp

    
    def save_model(self, request, menu, form, change):
        """First execute this body then save model as usual"""
        # Log the event
    
        super().save_model(request, menu, form, change) # maybe this can be edeleted with super.savaemodelr
        # uploaded_log = AuditLog.objects.create(
        #     menu_version=menu.version,
        #     phase="Uploaded file",
        #     status="Received"
        # )


        if menu.menu_file and not change:  # Only process on new uploads
            menu.user_id = request.user
            # uploaded_log.status = "Processed"
            # uploaded_log.save()
            try:
                menu_json = ai_call(menu)
                print("I am about to populate_menu_data")
                populate_menu_data(menu, menu_json)
                print("About to create MenuVersion FK!!!")
                if menu.restaurant.name:
                    print(f"Menu restaurant: {menu.restaurant}")

                    menu_version = MenuVersion.objects.create(restaurant=menu.restaurant)
                    print(f"Menu version: {menu_version.composite_id}")
                    menu.version = menu_version
                    menu.save()
                else:
                    raise ValueError("Restaurant must be set before creating MenuVersion")
            except Exception as e:
                self.message_user(request, f"Error processing menu: {str(e)}", level='ERROR')


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
    search_fields = ('name', 'description', 'menu_section')

@admin.register(DietaryRestriction)
class DietaryRestrictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(MenuVersion)
class MenuVersionAdmin(admin.ModelAdmin):
    list_display = ("id", "composite_id")

# @admin.register(AuditLog)
# class AuditLogAdmin(admin.ModelAdmin):
#     list_display = ('id', 'menu', 'status', 'phase', 'other', 'time_registered')
#     list_filter = ('status',)
#     #readonly_fields = ('menu', 'status', 'action', 'entity_affected', 'old_value', 'new_value')

