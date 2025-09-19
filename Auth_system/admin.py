from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
admin.site.register(User)

@admin.register(Company_type)
class CompanyTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# Register Company_info
@admin.register(Company_info)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('company_id', 'company_name', 'email', 'phone_number', 'type', 'domain')
    search_fields = ('company_name', 'email', 'domain')
    list_filter = ('type',)

# Register User_role
@admin.register(User_role)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'role')
    search_fields = ('role',)

# Register User_info
@admin.register(User_info)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'email', 'phone_number', 'gender', 'role', 'company')
    search_fields = ('name', 'email', 'phone_number', 'nid', 'passport')
    list_filter = ('gender', 'role', 'company', 'religion')
    readonly_fields = ('password',)
    
