
# # Create your models here.
# from django.db import models
# from django.contrib.auth.models import User
# # Worker availability choices
#     WORKER_STATUS_CHOICES = [
#         ('Available', 'Available'),
#         ('Busy', 'Busy'),
#         ('Off', 'Off'),
#     ]

# # Complaint model for students
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

    

# # Worker Profile
# class WorkerProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     status = models.CharField(max_length=10, choices=WORKER_STATUS_CHOICES, default='Available')

#     def __str__(self):
#         return self.user.username
#     # def __str__(self):
#     #     return f"{self.title} - {self.user.username}"

#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # Changed 'user' to 'student'
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     status = models.CharField(max_length=20, default='Pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#     category = models.CharField(max_length=50, blank=True)
#     image = models.ImageField(upload_to='complaint_images/', blank=True, null=True)
#     assigned_worker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_worker')

#     def __str__(self):
#         return f"{self.title} - {self.student.username}"  # student is the ForeignKey field

# from django.db import models
# from django.contrib.auth.models import User

# # -----------------------------
# # Worker availability choices
# WORKER_STATUS_CHOICES = [
#     ('Available', 'Available'),
#     ('Busy', 'Busy'),
# ]

# # Complaint status choices
# STATUS_CHOICES = [
#     ('Pending', 'Pending'),
#     ('Assigned', 'Assigned'),
#     ('Resolved', 'Resolved'),
# ]

# # Complaint category choices
# CATEGORY_CHOICES = [
#     ('Plumbing', 'Plumbing'),
#     ('Electrical', 'Electrical'),
#     ('Cleaning', 'Cleaning'),
#     ('Other', 'Other'),
# ]

# # -----------------------------
# # Worker Profile model
# class WorkerProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     status = models.CharField(max_length=10, choices=WORKER_STATUS_CHOICES, default='Available')

#     def __str__(self):
#         return self.user.username

# # -----------------------------
# # Complaint model
# class Complaint(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_complaints')  # The student who created
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
#     category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True)
#     image = models.ImageField(upload_to='complaint_images/', blank=True, null=True)
#     assigned_worker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_worker')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.title} - {self.user.username}"

#     # student = models.ForeignKey(User, on_delete=models.CASCADE)
#     # title = models.CharField(max_length=200)
#     # description = models.TextField()
#     # category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
#     # image = models.ImageField(upload_to='complaint_images/', blank=True, null=True)
#     # status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
#     # created_at = models.DateTimeField(auto_now_add=True)
#     # assigned_worker = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.SET_NULL, null=True, blank=True)

#     # def __str__(self):
#     #     return f"{self.title} - {self.status}"

from django.db import models
from django.contrib.auth.models import User

# -----------------------------
# Worker availability choices
WORKER_STATUS_CHOICES = [
    ('Available', 'Available'),
    ('Busy', 'Busy'),
    ('Off', 'Off'),
]

# Complaint status choices
STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Assigned', 'Assigned'),
    ('Resolved', 'Resolved'),
]

# Complaint category choices
CATEGORY_CHOICES = [
    ('Plumbing', 'Plumbing'),
    ('Electrical', 'Electrical'),
    ('Cleaning', 'Cleaning'),
    ('Other', 'Other'),
]

# -----------------------------
# Worker Profile model
class WorkerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=WORKER_STATUS_CHOICES, default='Available')

    def __str__(self):
        return self.user.username

# -----------------------------
# Complaint model
class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_complaints')  # The student who created
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True)
    image = models.ImageField(upload_to='complaint_images/', blank=True, null=True)
    assigned_worker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_worker')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
