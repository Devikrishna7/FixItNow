from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("student-dashboard/", views.student_dashboard, name="student_dashboard"),
    path('submit-complaint/', views.submit_complaint, name='submit_complaint'),
    path("worker-dashboard/", views.worker_dashboard, name="worker_dashboard"),
    path("mark-resolved/<int:complaint_id>/", views.mark_resolved, name="mark_resolved"),

    #  path('worker-dashboard/', views.worker_dashboard, name='worker_dashboard'),
    # path('mark-resolved/<int:complaint_id>/', views.mark_resolved, name='mark_resolved'),
    
]
