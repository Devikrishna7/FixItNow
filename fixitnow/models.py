# from django.db import models
# from django.contrib.auth.models import User

# # -----------------------------
# # Worker Profile
# # -----------------------------
# class WorkerProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     status = models.CharField(max_length=20, default='Available')  # Available, Busy, Offline

#     def __str__(self):
#         return f"{self.title} - {self.user.username}"


# # -----------------------------
# # Complaint Model
# # -----------------------------
# class Complaint(models.Model):
#     STATUS_CHOICES = [
#         ('Pending', 'Pending'),
#         ('Assigned', 'Assigned'),
#         ('Resolved', 'Resolved'),
#     ]

#     CATEGORY_CHOICES = [
#         ('Plumbing', 'Plumbing'),
#         ('Electrical', 'Electrical'),
#         ('Cleaning', 'Cleaning'),
#         ('Other', 'Other'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_complaints')  # student who created
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
#     assigned_worker = models.ForeignKey(
#         User,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='assigned_complaints'  # matches views.py queries
#     )
#     image = models.ImageField(upload_to='complaint_images/', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.title} - {self.status}"
from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('worker', 'Worker'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.username} ({self.role})"

# Worker Profile (optional extra details for workers)
class WorkerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='Available')  # Available, Busy, Offline

    def __str__(self):
        return f"{self.title} - {self.user.username}"


# Complaint Model
class Complaint(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Assigned', 'Assigned'),
        ('Resolved', 'Resolved'),
    ]

    CATEGORY_CHOICES = [
        ('Plumbing', 'Plumbing'),
        ('Electrical', 'Electrical'),
        ('Cleaning', 'Cleaning'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='student_complaints')
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    assigned_worker = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_complaints'
    )
    image = models.ImageField(upload_to='complaint_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.status}"
