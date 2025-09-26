
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseForbidden
from .models import Complaint, WorkerProfile, CustomUser
from django.contrib import messages

# -----------------------------
# Home Page
# -----------------------------
def index(request):
    return render(request, "index.html")

# -----------------------------
# Login Page
# -----------------------------

def login_view(request):
    
    # list(messages.get_messages(request))

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
            else:
                return redirect('student_dashboard')
        else:
            messages.error(request, "Invalid username or password")
            
    return render(request, "login.html")

# -----------------------------
# Logout
# -----------------------------
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


# -----------------------------
# Register Page (for students)
# -----------------------------
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        # Create a student user by default
        user = CustomUser.objects.create_user(username=username, password=password, role='student')
        user.save()
        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")

    return render(request, "register.html")

# -----------------------------
# Student Dashboard
# -----------------------------
@login_required(login_url="login")
def student_dashboard(request):
    if request.user.role != 'student':
        return HttpResponseForbidden("You are not authorized to view this page.")

    complaints = request.user.student_complaints.all().order_by("-created_at")
    return render(request, "student_dashboard.html", {"complaints": complaints})


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
        category = request.POST.get("category") or request.POST.get("complaint_type") or "Other"
        image = request.FILES.get("image")

        if title and description:
            Complaint.objects.create(
                user=request.user,
                title=title,
                description=description,
                category=category,
                image=image,
            )
            messages.success(request, "Complaint submitted successfully!")
            return redirect("student_dashboard")
        else:
            messages.error(request, "Please provide title and description.")

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
    return render(request, "worker_dashboard.html", {"complaints": complaints, "profile": profile})


# -----------------------------
# Worker marks complaint as resolved
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
    
    if request.user.role == 'admin':
        return redirect("admin_dashboard")
    else:
        return redirect("worker_dashboard")

# -----------------------------
# Admin Dashboard
# -----------------------------
@login_required(login_url="login")
def admin_dashboard(request):
    
    if request.user.role != 'admin':
        return HttpResponseForbidden("You are not authorized to view this page.")

    complaints = Complaint.objects.all().order_by("-created_at")
    workers = WorkerProfile.objects.all()
     # Fetch all workers with their user info
    workers = WorkerProfile.objects.select_related('user').all()
    return render(request, "admin_dashboard.html", {"complaints": complaints, "workers": workers})


# -----------------------------
# Assign worker to complaint
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

            # Assign the worker to complaint
            complaint.assigned_worker = worker_profile.user
            complaint.status = "Assigned"
            complaint.save()

            # Update worker status to Busy automatically
            worker_profile.status = "Busy"
            worker_profile.save()

            messages.success(request, f"Worker '{worker_profile.user.username}' assigned successfully and status set to Busy!")

    return redirect("admin_dashboard")

# -----------------------------
# Add a worker
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

        # Create worker user
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role='worker'
        )

        # save phone number & status into WorkerProfile
        WorkerProfile.objects.create(
            user=user,
            phone_number=phone_number,
            status=status
        )

        messages.success(request, f"Worker '{username}' added successfully!")
        return redirect("admin_dashboard")

    return render(request, "add_worker.html")

# -----------------------------
# Update a worker
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

        # Update user model
        user = worker_profile.user
        if first_name: user.first_name = first_name
        if last_name: user.last_name = last_name
        if username: user.username = username
        if email: user.email = email
        user.save()

        # Update worker profile
        if phone_number: worker_profile.phone_number = phone_number
        if status in ["Available", "Busy", "Offline"]: worker_profile.status = status
        worker_profile.save()

        messages.success(request, f"Worker '{user.username}' updated successfully!")
        return redirect("admin_dashboard")

    return render(request, "update_worker.html", {"worker_profile": worker_profile})

# -----------------------------
# Delete a worker
# -----------------------------
@login_required(login_url="login")
def delete_worker(request, worker_id):
    if request.user.role != 'admin':
        return HttpResponseForbidden("You are not authorized to perform this action.")

    worker = get_object_or_404(CustomUser, id=worker_id, role='worker')
    worker.delete()
    messages.success(request, "Worker deleted successfully!")
    return redirect("admin_dashboard")
