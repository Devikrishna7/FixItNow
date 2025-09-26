from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, WorkerProfile, StudentProfile, Complaint

# -----------------------------
# Inline Worker Profile (inside UserAdmin)
# -----------------------------
class WorkerProfileInline(admin.StackedInline):
    model = WorkerProfile
    can_delete = False
    extra = 0
    verbose_name_plural = "Worker Profile"

# -----------------------------
# Inline Student Profile
# -----------------------------
class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    extra = 0
    verbose_name_plural = "Student Profile"


# -----------------------------
# Custom User Admin
# -----------------------------
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'get_phone', 'get_department', 'get_admission_number', 'get_year_of_admission')
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
        Show the correct inline based on role:
        - WorkerProfile for workers
        - StudentProfile for students
        """
        if obj:
            if obj.role == "worker":
                return [WorkerProfileInline(self.model, self.admin_site)]
            elif obj.role == "student":
                return [StudentProfileInline(self.model, self.admin_site)]
        return []

      # Extra fields for student profile
    def get_phone(self, obj):
        return obj.studentprofile.phone_number if hasattr(obj, "studentprofile") else "-"
    get_phone.short_description = "Phone"

    def get_department(self, obj):
        return obj.studentprofile.department if hasattr(obj, "studentprofile") else "-"
    get_department.short_description = "Department"

    def get_admission_number(self, obj):
        return obj.studentprofile.admission_number if hasattr(obj, "studentprofile") else "-"
    get_admission_number.short_description = "Admission No."

    def get_year_of_admission(self, obj):
        return obj.studentprofile.year_of_admission if hasattr(obj, "studentprofile") else "-"
    get_year_of_admission.short_description = "Year"


# -----------------------------
# Worker Profile Admin
# -----------------------------
class WorkerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'title')


# -----------------------------
# Student Profile Admin
# -----------------------------
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'department', 'admission_number', 'year_of_admission')
    list_filter = ('department', 'year_of_admission')
    search_fields = ('user__username', 'admission_number', 'department')

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
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(Complaint, ComplaintAdmin)
