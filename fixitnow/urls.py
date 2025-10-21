from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import login_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.login_view, name='login'),
    path("logout/", views.logout_view, name="logout"),
    
    path("student-dashboard/", views.student_dashboard, name="student_dashboard"),
    path('submit-complaint/', views.submit_complaint, name='submit_complaint'),
    
    path("worker-dashboard/", views.worker_dashboard, name="worker_dashboard"),
    path("mark-resolved/<int:complaint_id>/", views.mark_resolved, name="mark_resolved"),
    
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin/complaint-table/", views.admin_complaint_table, name="admin_complaint_table"),
    path("admin/complaint-chart/", views.admin_complaint_chart, name="admin_complaint_chart"),
    
    path("add-worker/", views.add_worker, name="add_worker"),
    path("update-worker/<int:worker_id>/", views.update_worker, name="update_worker"),
    path("delete-worker/<int:worker_id>/", views.delete_worker, name="delete_worker"),
    path("assign-worker/<int:complaint_id>/", views.assign_worker, name="assign_worker"),
    
    path("add-student/", views.add_student, name="add_student"),
    path("edit-student/<int:student_id>/", views.edit_student, name="edit_student"),

]
