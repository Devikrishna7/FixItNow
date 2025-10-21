
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import authenticate, login as auth_login, logout
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required

# from django.contrib.auth.views import LoginView
# from django.http import HttpResponseForbidden
# from .models import Complaint, WorkerProfile, StudentProfile, CustomUser,Complaint, Worker, Student
# from django.contrib.auth.hashers import make_password
# from django.core.mail import send_mail
# from .models import Complaint
# from django.db.models import Count

# # -----------------------------
# # Home Page
# # -----------------------------
# # @login_required(login_url='login')
# def index(request):
#     return render(request, "index.html")

# # -----------------------------
# # Login Page
# # -----------------------------

# def login_view(request):
    
#     # list(messages.get_messages(request))

#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             auth_login(request, user)
#             if user.role == 'admin':
#                 return redirect('admin_dashboard')
#             elif user.role == 'worker':
#                 return redirect('worker_dashboard')
#             else:
#                 return redirect('student_dashboard')
#         else:
#             messages.error(request, "Invalid username or password")
            
#     return render(request, "login.html")

# # -----------------------------
# # Logout
# # -----------------------------
# def logout_view(request):
#     logout(request)
#     messages.info(request, "You have been logged out.")
#     return redirect("login")

# # -----------------------------
# # Student Dashboard
# # -----------------------------

# @login_required(login_url="login")
# def student_dashboard(request):
#     if request.user.role != 'student':
#         return HttpResponseForbidden("You are not authorized to view this page.")
    
#     # Access student profile if needed
#     student_profile = getattr(request.user, 'studentprofile', None)
    
#     complaints = request.user.student_complaints.all().order_by("-created_at")
#     return render(request, "student_dashboard.html", {
#         "complaints": complaints,
#         "profile": student_profile
#     })

# # -----------------------------
# # Submit Complaint
# # -----------------------------

# @login_required(login_url="login")
# def submit_complaint(request):
#     # Only students can submit complaints
#     if request.user.role != 'student':
#         return HttpResponseForbidden("You are not authorized to submit complaints.")

#     if request.method == "POST":
#         title = request.POST.get("title")
#         description = request.POST.get("description")
#         category = (
#             request.POST.get("category")
#             or request.POST.get("complaint_type")
#             or "Other"
#         )
#         image = request.FILES.get("image")

#         if title and description:
#             # Create complaint first
#             complaint = Complaint.objects.create(
#                 user=request.user,
#                 title=title,
#                 description=description,
#                 category=category,
#                 image=image,
#                 status="Pending"
#             )

#             # Try to auto-assign available worker based on specialization
#             available_worker = WorkerProfile.objects.filter(
#                 status="Available",
#                 specialization__iexact=category
#             ).first()

#             if available_worker:
#                 complaint.assigned_worker = available_worker.user
#                 complaint.status = "Assigned"
#                 complaint.save()

#                 # Update worker status to busy
#                 available_worker.status = "Busy"
#                 available_worker.save()

#                 messages.success(
#                     request,
#                     f"Complaint submitted and assigned to worker: {available_worker.user.username}."
#                 )
#             else:
#                 messages.warning(
#                     request,
#                     "Complaint submitted but no available worker found for this category."
#                 )

#             return redirect("student_dashboard")

#         else:
#             messages.error(request, "Please provide both title and description.")

#     return render(request, "submit_complaint.html")
# # -----------------------------
# # Worker Dashboard
# # -----------------------------
# @login_required(login_url="login")
# def worker_dashboard(request):
    
#     if request.user.role != 'worker':
#         return HttpResponseForbidden("You are not authorized to view this page.")

#     profile, created = WorkerProfile.objects.get_or_create(user=request.user)

#     if request.method == "POST":
#         status = request.POST.get("status")
#         if status in ["Available", "Busy", "Offline"]:
#             profile.status = status
#             profile.save()

#     complaints = Complaint.objects.filter(assigned_worker=request.user).order_by('-created_at')
#     return render(request, "worker_dashboard.html", {"complaints": complaints, "profile": profile})


# # -----------------------------
# # Worker marks complaint as resolved
# # -----------------------------

# @login_required(login_url="login")
# def mark_resolved(request, complaint_id):
#     complaint = get_object_or_404(Complaint, id=complaint_id)

#     if request.user.role == 'worker' and complaint.assigned_worker != request.user:
#         return HttpResponseForbidden("You are not authorized to perform this action.")

#     elif request.user.role not in ['worker', 'admin']:
#         return HttpResponseForbidden("You are not authorized to perform this action.")

#     complaint.status = "Resolved"
#     complaint.save()
#     messages.success(request, "Complaint marked as resolved.")
    
#     if request.user.role == 'admin':
#         return redirect("admin_dashboard")
#     else:
#         return redirect("worker_dashboard")

# # -----------------------------
# # Admin Dashboard
# # -----------------------------
# @login_required(login_url="login")
# def admin_dashboard(request):
    
#     if request.user.role != 'admin':
#         return HttpResponseForbidden("You are not authorized to view this page.")

#     complaints = Complaint.objects.all().order_by("-created_at")
#     workers = WorkerProfile.objects.all()
#      # Fetch all workers with their user info
#     workers = WorkerProfile.objects.select_related('user').all()
#     students = StudentProfile.objects.select_related('user').all()  # Fetch students
#     return render(request, "admin_dashboard.html", {"complaints": complaints, "workers": workers, "students": students})

# # Admin: Complaint Table
# def admin_complaint_table(request):
#     complaints = Complaint.objects.all().order_by('-created_at')
#     return render(request, 'admin/complaint_table.html', {'complaints': complaints})

# # Admin: Complaint Charts
# def admin_complaint_chart(request):
#     # Example: count complaints by status
#     status_data = Complaint.objects.values('status').annotate(count=Count('status'))
    
#     # Prepare data for chart.js
#     labels = [item['status'] for item in status_data]
#     counts = [item['count'] for item in status_data]
    
#     return render(request, 'admin/complaint_chart.html', {'labels': labels, 'counts': counts})

# # -----------------------------
# # Add Student (Admin only)
# # -----------------------------
# @login_required(login_url="login")
# def add_student(request):
#     if request.user.role != 'admin':
#         return HttpResponseForbidden("You are not authorized to perform this action.")

#     if request.method == "POST":
#         first_name = request.POST.get("first_name")
#         last_name = request.POST.get("last_name")
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         confirm_password = request.POST.get("confirm_password")
#         email = request.POST.get("email")
#         phone_number = request.POST.get("phone_number")
#         department = request.POST.get("department")
#         admission_number = request.POST.get("admission_number")
#         year_of_admission = request.POST.get("year_of_admission")

#         # Password match check
#         if password != confirm_password:
#             messages.error(request, "Passwords do not match")
#             return redirect("add_student")

#         # Username uniqueness
#         if CustomUser.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists")
#             return redirect("add_student")

#         # Email uniqueness
#         if CustomUser.objects.filter(email=email).exists():
#             messages.error(request, "Email already exists")
#             return redirect("add_student")

#         # Create student user
#         user = CustomUser.objects.create_user(
#             username=username,
#             password=password,
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             role='student'
#         )

#         # Save extra info in StudentProfile
#         StudentProfile.objects.create(
#             user=user,
#             phone_number=phone_number,
#             department=department,
#             admission_number=admission_number,
#             year_of_admission=year_of_admission
#         )

#         messages.success(request, f"Student '{username}' added successfully!")
#         return redirect("admin_dashboard")

#     return render(request, "add_student.html")
# # -----------------------------
# # Assign worker to complaint
# # -----------------------------

# @login_required(login_url="login")
# def assign_worker(request, complaint_id):
#     if request.user.role != 'admin':
#         return HttpResponseForbidden("You are not authorized to perform this action.")

#     complaint = get_object_or_404(Complaint, id=complaint_id)
#     available_workers = WorkerProfile.objects.filter(status='Available').select_related('user')

#     if request.method == "POST":
#         worker_id = request.POST.get("worker_id")
#         if worker_id:
#             worker_profile = get_object_or_404(WorkerProfile, id=worker_id)

#             # Assign the worker to complaint
#             complaint.assigned_worker = worker_profile.user
#             complaint.status = "Assigned"
#             complaint.save()

#             # Update worker status to Busy automatically
#             worker_profile.status = "Busy"
#             worker_profile.save()

#             messages.success(request, f"Worker '{worker_profile.user.username}' assigned successfully and status set to Busy!")

#     return redirect("admin_dashboard")

# # -----------------------------
# # Add a worker
# # -----------------------------

# @login_required(login_url="login")
# def add_worker(request):
#     if request.user.role != 'admin':
#         return HttpResponseForbidden("You are not authorized to perform this action.")

#     if request.method == "POST":
#         first_name = request.POST.get("first_name")
#         last_name = request.POST.get("last_name")
#         username = request.POST.get("username")
#         email = request.POST.get("email")
#         phone_number = request.POST.get("phone_number")
#         password = request.POST.get("password")
#         confirm_password = request.POST.get("confirm_password")
#         status = request.POST.get("status")

#         if password != confirm_password:
#             messages.error(request, "Passwords do not match")
#             return redirect("add_worker")

#         if CustomUser.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists")
#             return redirect("add_worker")

#         # Create worker user
#         user = CustomUser.objects.create_user(
#             username=username,
#             password=password,
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             role='worker'
#         )

#         # save phone number & status into WorkerProfile
#         WorkerProfile.objects.create(
#             user=user,
#             phone_number=phone_number,
#             status=status
#         )

#         messages.success(request, f"Worker '{username}' added successfully!")
#         return redirect("admin_dashboard")

#     return render(request, "add_worker.html")

# # -----------------------------
# # Update a worker
# # -----------------------------

# @login_required(login_url="login")
# def update_worker(request, worker_id):
#     if request.user.role != 'admin':
#         return HttpResponseForbidden("You are not authorized to perform this action.")

#     worker_profile = get_object_or_404(WorkerProfile, user__id=worker_id)

#     if request.method == "POST":
#         first_name = request.POST.get("first_name")
#         last_name = request.POST.get("last_name")
#         username = request.POST.get("username")
#         email = request.POST.get("email")
#         phone_number = request.POST.get("phone_number")
#         status = request.POST.get("status")

#         # Update user model
#         user = worker_profile.user
#         if first_name: user.first_name = first_name
#         if last_name: user.last_name = last_name
#         if username: user.username = username
#         if email: user.email = email
#         user.save()

#         # Update worker profile
#         if phone_number: worker_profile.phone_number = phone_number
#         if status in ["Available", "Busy", "Offline"]: worker_profile.status = status
#         worker_profile.save()

#         messages.success(request, f"Worker '{user.username}' updated successfully!")
#         return redirect("admin_dashboard")

#     return render(request, "update_worker.html", {"worker_profile": worker_profile})

# # -----------------------------
# # Delete a worker
# # -----------------------------
# @login_required(login_url="login")
# def delete_worker(request, worker_id):
#     if request.user.role != 'admin':
#         return HttpResponseForbidden("You are not authorized to perform this action.")

#     worker = get_object_or_404(CustomUser, id=worker_id, role='worker')
#     worker.delete()
#     messages.success(request, "Worker deleted successfully!")
#     return redirect("admin_dashboard")
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Count
from django.core.mail import send_mail

from .models import CustomUser, Complaint, WorkerProfile, StudentProfile

# -----------------------------
# Home Page
# -----------------------------
def index(request):
    return render(request, "index.html")


# -----------------------------
# Login Page
# -----------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'worker':
                return redirect('worker_dashboard')
            elif user.role == 'student':
                return redirect('student_dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


# -----------------------------
# Logout
# -----------------------------
@login_required(login_url="login")
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


# -----------------------------
# Student Dashboard
# -----------------------------
@login_required(login_url="login")
def student_dashboard(request):
    if request.user.role != 'student':
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    student_profile = getattr(request.user, 'studentprofile', None)
    complaints = request.user.student_complaints.all().order_by("-created_at")

    return render(request, "student_dashboard.html", {
        "complaints": complaints,
        "profile": student_profile
    })


# -----------------------------
# Submit Complaint
# -----------------------------
@login_required(login_url="login")
def submit_complaint(request):
    if request.user.role != 'student':
        return HttpResponseForbidden("You are not authorized to submit complaints.")

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        category = (
            request.POST.get("category")
            or request.POST.get("complaint_type")
            or "Other"
        )
        image = request.FILES.get("image")

        if title and description:
            complaint = Complaint.objects.create(
                user=request.user,
                title=title,
                description=description,
                category=category,
                image=image,
                status="Pending"
            )

            # Auto-assign available worker (if any)
            available_worker = WorkerProfile.objects.filter(
                status="Available",
                specialization__iexact=category
            ).first()

            if available_worker:
                complaint.assigned_worker = available_worker.user
                complaint.status = "Assigned"
                complaint.save()

                available_worker.status = "Busy"
                available_worker.save()

                messages.success(
                    request,
                    f"Complaint submitted and assigned to worker: {available_worker.user.username}."
                )
            else:
                messages.warning(
                    request,
                    "Complaint submitted but no available worker found for this category."
                )

            return redirect("student_dashboard")

        messages.error(request, "Please provide both title and description.")

    return render(request, "submit_complaint.html")


# -----------------------------
# Worker Dashboard
# -----------------------------
@login_required(login_url="login")
def worker_dashboard(request):
    if request.user.role != 'worker':
        return HttpResponseForbidden("You are not authorized to view this page.")

    profile, created = WorkerProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        status = request.POST.get("status")
        if status in ["Available", "Busy", "Offline"]:
            profile.status = status
            profile.save()

    complaints = Complaint.objects.filter(assigned_worker=request.user).order_by('-created_at')

    return render(request, "worker_dashboard.html", {
        "complaints": complaints,
        "profile": profile
    })


# -----------------------------
# Worker Marks Complaint as Resolved
# -----------------------------
@login_required(login_url="login")
def mark_resolved(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.user.role == 'worker' and complaint.assigned_worker != request.user:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    elif request.user.role not in ['worker', 'admin']:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    complaint.status = "Resolved"
    complaint.save()
    messages.success(request, "Complaint marked as resolved.")
    
    # Send email to student
    if complaint.user.email:
        send_mail(
            'Complaint Resolved',
            f'Your complaint "{complaint.title}" has been resolved.',
            'admin@example.com',
            [complaint.user.email],
            fail_silently=True
        )

    
    if request.user.role == 'admin':
        return redirect("admin_dashboard")
    return redirect("worker_dashboard")


# -----------------------------
# Admin Dashboard
# -----------------------------
@login_required(login_url="login")
def admin_dashboard(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("You are not authorized to view this page.")

    complaints = Complaint.objects.all().order_by("-created_at")
    workers = WorkerProfile.objects.select_related('user').all()
    students = StudentProfile.objects.select_related('user').all()
     # Calculate complaint status counts
    pending_count = Complaint.objects.filter(status="Pending").count()
    assigned_count = Complaint.objects.filter(status="Assigned").count()
    resolved_count = Complaint.objects.filter(status="Resolved").count()

    context = {
        "complaints": complaints,
        "workers": workers,
        "students": students,
        "pending_count": pending_count,
        "assigned_count": assigned_count,
        "resolved_count": resolved_count,
    }
    return render(request, "admin_dashboard.html", context)
    #               {
    #     "complaints": complaints,
    #     "workers": workers,
    #     "students": students
    # })




# -----------------------------
# Add Student (Admin only)
# -----------------------------
@login_required(login_url="login")
def add_student(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("You are not authorized to perform this action.")

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        department = request.POST.get("department")
        admission_number = request.POST.get("admission_number")
        year_of_admission = request.POST.get("year_of_admission")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("add_student")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("add_student")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("add_student")

        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role='student'
        )

        StudentProfile.objects.create(
            user=user,
            phone_number=phone_number,
            department=department,
            admission_number=admission_number,
            year_of_admission=year_of_admission
        )

        messages.success(request, f"Student '{username}' added successfully!")
        return redirect("admin_dashboard")

    return render(request, "add_student.html")
# -----------------------------
# edit student
# -----------------------------
@login_required(login_url="login")
def edit_student(request, student_id):
    # Fetch the student user using CustomUser
    student_user = get_object_or_404(CustomUser, id=student_id, role='student')
    student_profile = getattr(student_user, 'studentprofile', None)

    if request.method == "POST":
        # Update User fields
        student_user.first_name = request.POST.get("first_name")
        student_user.last_name = request.POST.get("last_name")
        student_user.username = request.POST.get("username")
        student_user.email = request.POST.get("email")
        student_user.save()

        # Update StudentProfile fields
        if student_profile:
            student_profile.phone_number = request.POST.get("phone_number")
            student_profile.department = request.POST.get("department")
            student_profile.admission_number = request.POST.get("admission_number")
            student_profile.year_of_admission = request.POST.get("year_of_admission")
            student_profile.save()

        messages.success(request, f"Student '{student_user.username}' updated successfully!")
        return redirect("admin_dashboard")

    return render(request, "edit_student.html", {
        "student_user": student_user,
        "student_profile": student_profile
    })


# -----------------------------
# Add Worker (Admin only)
# -----------------------------
@login_required(login_url="login")
def add_worker(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("You are not authorized to perform this action.")

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        status = request.POST.get("status")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("add_worker")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("add_worker")

        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role='worker'
        )

        WorkerProfile.objects.create(
            user=user,
            phone_number=phone_number,
            status=status
        )

        messages.success(request, f"Worker '{username}' added successfully!")
        return redirect("admin_dashboard")

    return render(request, "add_worker.html")

# -----------------------------
# Assign Worker to Complaint
# -----------------------------
@login_required(login_url="login")
def assign_worker(request, complaint_id):
    if request.user.role != 'admin':
        return HttpResponseForbidden("You are not authorized to perform this action.")

    complaint = get_object_or_404(Complaint, id=complaint_id)
    available_workers = WorkerProfile.objects.filter(status='Available').select_related('user')

    if request.method == "POST":
        worker_id = request.POST.get("worker_id")
        if worker_id:
            worker_profile = get_object_or_404(WorkerProfile, id=worker_id)

            # Assign the worker
            complaint.assigned_worker = worker_profile.user
            complaint.status = "Assigned"
            complaint.save()

            # Set worker as busy
            worker_profile.status = "Busy"
            worker_profile.save()

            messages.success(request, f"Worker '{worker_profile.user.username}' assigned successfully!")

    return redirect("admin_dashboard")
# -----------------------------
# Update Worker
# -----------------------------
@login_required(login_url="login")
def update_worker(request, worker_id):
    if request.user.role != 'admin':
        return HttpResponseForbidden("You are not authorized to perform this action.")

    worker_profile = get_object_or_404(WorkerProfile, user__id=worker_id)

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        status = request.POST.get("status")

        user = worker_profile.user
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.save()

        worker_profile.phone_number = phone_number
        worker_profile.status = status
        worker_profile.save()

        messages.success(request, f"Worker '{user.username}' updated successfully!")
        return redirect("admin_dashboard")

    return render(request, "update_worker.html", {"worker_profile": worker_profile})


# -----------------------------
# Delete Worker
# -----------------------------
@login_required(login_url="login")
def delete_worker(request, worker_id):
    if request.user.role != 'admin':
        return HttpResponseForbidden("You are not authorized to perform this action.")

    worker = get_object_or_404(CustomUser, id=worker_id, role='worker')
    worker.delete()
    messages.success(request, "Worker deleted successfully!")
    return redirect("admin_dashboard")

# -----------------------------
# Complaint Table
# -----------------------------
@login_required(login_url="login")
def admin_complaint_table(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'admin/complaint_table.html', {'complaints': complaints})


# -----------------------------
# Complaint Chart Page
# -----------------------------
@login_required(login_url="login")
def admin_complaint_chart(request):
    status_data = Complaint.objects.values('status').annotate(count=Count('status'))
    labels = [item['status'] for item in status_data]
    counts = [item['count'] for item in status_data]

    return render(request, 'admin/complaint_chart.html', {
        'labels': labels,
        'counts': counts
    })

