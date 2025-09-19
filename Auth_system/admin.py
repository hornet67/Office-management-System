from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import *

# -------------------------
# User model (custom)
# -------------------------
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'age', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    
    
# -------------------------
# Company type
# -------------------------
@admin.register(Company_type)
class CompanyTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    
    

# -------------------------
# Company info
# -------------------------
@admin.register(Company_info)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('company_id', 'company_name', 'email', 'phone_number', 'type', 'domain')
    search_fields = ('company_name', 'email', 'domain')
    list_filter = ('type',)
    
    
# -------------------------
# User Role
# -------------------------

@admin.register(User_role)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'role')
    search_fields = ('role',)


# -------------------------
# Activated Users
# -------------------------

# @admin.register(User_info)
# class UserInfoAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'role', 'company', 'activated_by_name', 'activated_at')
#     list_filter = ('role', 'company')
#     search_fields = ('name', 'email', 'company__company_name')
# # Register User_info

@admin.register(User_info)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'email', 'phone_number', 'gender', 'role', 'company', 'activated_by','activated_at')
    search_fields = ('name', 'email', 'phone_number', 'nid', 'passport')
    list_filter = ('gender', 'role', 'company', 'religion')
    readonly_fields = ('password',)



# -------------------------
# Pending Users
# -------------------------
@admin.register(PendingUser)
class PendingUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'role', 'company', 'registered_at', 'activate_button','delete_button')
    list_filter = ('role', 'company')
    search_fields = ('name', 'email', 'company__company_name')

    # Activate button
    def activate_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Activate</a>',
            f'activate/{obj.id}/'
        )
    activate_button.short_description = 'Activate User'
    activate_button.allow_tags = True
   
   
    # Delete button
    def delete_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Delete</a>',
            f'delete/{obj.id}/'
        )
    delete_button.short_description = 'Delete User'
    delete_button.allow_tags = True

    # Custom admin URL
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('activate/<int:pending_user_id>/', self.admin_site.admin_view(self.activate_user), name='activate-user'),
            path('delete/<int:pending_user_id>/', self.admin_site.admin_view(self.delete_user), name='delete-user'),
        ]
        return custom_urls + urls

    # View to handle activation
    def activate_user(self, request, pending_user_id):
        activating_user = request.user  # Admin who is activating
        user_info = activate_pending_user(pending_user_id, activating_user)
        self.message_user(request, f'User "{user_info.name}" has been activated successfully.')
        from django.shortcuts import redirect
        return redirect('/admin/Auth_system/pendinguser/')
    
    # View to handle deletion
    def delete_user(self, request, pending_user_id):
        from django.shortcuts import redirect, get_object_or_404
        pending_user = get_object_or_404(PendingUser, pk=pending_user_id)
        pending_user.delete()
        self.message_user(request, f'Pending user "{pending_user.name}" has been deleted.', level='warning')
        return redirect('/admin/Auth_system/pendinguser/')
    
