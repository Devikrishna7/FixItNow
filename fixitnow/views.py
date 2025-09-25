

# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login as auth_login, logout
# from django.contrib.auth.models import User
# from django.contrib import messages
# from .models import Complaint
# from .forms import ComplaintForm
# from django.contrib.auth.decorators import login_required

# from .models import Complaint, WorkerProfile

#final
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Complaint, WorkerProfile
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
            return redirect("student_dashboard")
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
# Register Page
# -----------------------------

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")

    return render(request, "register.html")
# -----------------------------
# student Dashboard
# -----------------------------

@login_required(login_url="login")
def student_dashboard(request):
    # <-- FIXED: use the related_name defined on the Complaint model
    complaints = request.user.student_complaints.all().order_by("-created_at")
    return render(request, "student_dashboard.html", {"complaints": complaints})
# -----------------------------
# Submit Complaint
# -----------------------------

@login_required(login_url="login")
def submit_complaint(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        # support both possible form field names:
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
# # -----------------------------
# # Worker Dashboard
# # -----------------------------

# -----------------------------
# Mark Complaint as Resolved
# -----------------------------

@login_required(login_url="login")
def worker_dashboard(request):
    profile, created = WorkerProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        status = request.POST.get("status")
        if status in ["Available", "Busy", "Off"]:
            profile.status = status
            profile.save()

    complaints = Complaint.objects.filter(assigned_worker=request.user)
    return render(request, "worker_dashboard.html", {"complaints": complaints, "profile": profile})


@login_required(login_url="login")
def mark_resolved(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id, assigned_worker=request.user)
    complaint.status = "Resolved"
    complaint.save()
    messages.success(request, "Complaint marked as resolved.")
    return redirect("worker_dashboard")
