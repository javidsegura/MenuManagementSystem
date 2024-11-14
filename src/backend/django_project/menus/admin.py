""" Specify the models you want to display in the admin interface """

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html  # Add this import
from .models import (
    User,
    Post,
    MenuVersion,
    Restaurant,
    OpeningHours,
    Menu,
    MenuItem,
    DietaryRestriction,
    AuditLog
)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff') # represents the columns in the admin interface
    list_filter = ('is_staff', 'is_superuser') # filter based upon the fields
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('country', 'city', 'state', 'zip', 'street')}),
    )

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'phone', 'email')
    search_fields = ('name', 'city')

@admin.register(OpeningHours)
class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'open_time', 'close_time')
    list_filter = ('day_of_week',)

@admin.register(MenuVersion)
class MenuVersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restaurant', 'time_upload')
    list_filter = ('time_upload', 'restaurant')

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'section', 'menu_version', 'active_status', 'available_from', 'available_until', 'pdf_link')
    list_filter = ('active_status', 'available_from', 'available_until')
    
    def pdf_link(self, obj):
        if obj.menuPdf:
            return format_html('<a href="{}" target="_blank">View PDF</a>', obj.menuPdf.url)
        return '-'
    pdf_link.short_description = 'Menu PDF'
    

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu', 'price', 'currency', 'available')
    list_filter = ('available', 'currency', 'menu')
    search_fields = ('name', 'description')

@admin.register(DietaryRestriction)
class DietaryRestrictionAdmin(admin.ModelAdmin):
    list_display = ('description',)
    search_fields = ('description',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'upload_time')
    list_filter = ('upload_time',)

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('menu', 'status', 'action', 'entity_affected')
    list_filter = ('status',)
    readonly_fields = ('menu', 'status', 'action', 'entity_affected', 'old_value', 'new_value')