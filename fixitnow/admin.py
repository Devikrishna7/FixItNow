# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser, WorkerProfile, Complaint

# # -----------------------------
# # Custom User Admin
# # -----------------------------
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

# # -----------------------------
# # Worker Profile Admin
# # -----------------------------
# class WorkerProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'title', 'status')
#     list_filter = ('status',)
#     search_fields = ('user__username', 'title')

# # -----------------------------
# # Complaint Admin
# # -----------------------------
# class ComplaintAdmin(admin.ModelAdmin):
#     list_display = ('title', 'user', 'assigned_worker', 'status', 'category', 'created_at')
#     list_filter = ('status', 'category')
#     search_fields = ('title', 'user__username', 'assigned_worker__username')

# # -----------------------------
# # Register models
# # -----------------------------
# admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(WorkerProfile, WorkerProfileAdmin)
# admin.site.register(Complaint, ComplaintAdmin)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, WorkerProfile, Complaint

# -----------------------------
# Inline Worker Profile (inside UserAdmin)
# -----------------------------
class WorkerProfileInline(admin.StackedInline):
    model = WorkerProfile
    can_delete = False
    extra = 0
    verbose_name_plural = "Worker Profile"


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

    def get_inline_instances(self, request, obj=None):
        """
        Show WorkerProfile inline only if the user is a worker.
        """
        if obj and obj.role == "worker":
            return [WorkerProfileInline(self.model, self.admin_site)]
        return []


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

    def get_form(self, request, obj=None, **kwargs):
        """
        Show only available workers when assigning a complaint.
        """
        form = super().get_form(request, obj, **kwargs)
        if 'assigned_worker' in form.base_fields:
            # show only workers whose WorkerProfile.status is 'Available'
            form.base_fields['assigned_worker'].queryset = CustomUser.objects.filter(
                role='worker',
                workerprofile__status='Available'
            )
        return form


# -----------------------------
# Register models
# -----------------------------
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(WorkerProfile, WorkerProfileAdmin)
admin.site.register(Complaint, ComplaintAdmin)
