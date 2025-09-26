from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

DEPARTMENT_CHOICES = [
    ('BTech', 'B.Tech'),
    ('MTech', 'M.Tech'),
    ('MBA', 'MBA'),
    ('MCA', 'MCA'),
    ('PhD', 'PhD'),
]

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('worker', 'Worker'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.username} ({self.role})"


class WorkerProfile(models.Model):
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Busy', 'Busy'),
        ('Offline', 'Offline'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'worker'})
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')

    def __str__(self):
        return self.user.username


class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES)
    admission_number = models.CharField(max_length=50)
    year_of_admission = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username



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

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='student_complaints',
                             limit_choices_to={'role': 'student'})
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    assigned_worker = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_complaints',
        limit_choices_to={'role': 'worker'}
    )

    image = models.ImageField(upload_to='complaint_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.status}"

    def save(self, *args, **kwargs):
        """
        - If assigned_worker changed, free the old worker (set Available).
        - If assigned_worker exists and status != Resolved, set worker Busy.
        - If status == Resolved, mark assigned worker Available.
        """
        # capture old assigned worker (if any)
        old_assigned = None
        if self.pk:
            try:
                old = Complaint.objects.get(pk=self.pk)
                old_assigned = old.assigned_worker
            except Complaint.DoesNotExist:
                old_assigned = None

        super().save(*args, **kwargs) 

        # If assigned worker changed, free old worketr
        if old_assigned and old_assigned != self.assigned_worker:
            try:
                wp_old = WorkerProfile.objects.get(user=old_assigned)
                wp_old.status = 'Available'
                wp_old.save()
            except WorkerProfile.DoesNotExist:
                pass

        # If current assigned worker exists, update their status
        if self.assigned_worker:
            try:
                wp_new = WorkerProfile.objects.get(user=self.assigned_worker)
                if self.status == 'Resolved':
                    wp_new.status = 'Available'
                else:
                    wp_new.status = 'Busy'
                wp_new.save()
            except WorkerProfile.DoesNotExist:
                pass
        # If no assigned worker and status is Assigned, optionally set complaint back to Pending

def create_worker_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'worker':
        WorkerProfile.objects.get_or_create(user=instance, title="New Worker")


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'worker':
            WorkerProfile.objects.get_or_create(user=instance)