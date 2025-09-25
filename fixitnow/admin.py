# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser, WorkerProfile, Complaint

# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
#     list_filter = ('role', 'is_staff', 'is_active')
#     fieldsets = (
#         (None, {'fields': ('username', 'email', 'password', 'role')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
#         ),
#     )
#     search_fields = ('username', 'email')
#     ordering = ('username',)

# admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(WorkerProfile)
# admin.site.register(Complaint)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, WorkerProfile, Complaint

# -----------------------------
# Custom User Admin
# -----------------------------
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    
    search_fields = ('username', 'email')
    ordering = ('username',)

# -----------------------------
# Worker Profile Admin
# -----------------------------
class WorkerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'title')

# -----------------------------
# Complaint Admin
# -----------------------------
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'assigned_worker', 'status', 'category', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('title', 'user__username', 'assigned_worker__username')

# -----------------------------
# Register models
# -----------------------------
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(WorkerProfile, WorkerProfileAdmin)
admin.site.register(Complaint, ComplaintAdmin)
