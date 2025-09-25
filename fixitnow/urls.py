from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import login_view


urlpatterns = [
    path("", views.index, name="index"),
    
    path('login/', views.login_view, name='login'),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("student-dashboard/", views.student_dashboard, name="student_dashboard"),
    path('submit-complaint/', views.submit_complaint, name='submit_complaint'),
    path("worker-dashboard/", views.worker_dashboard, name="worker_dashboard"),
    path("mark-resolved/<int:complaint_id>/", views.mark_resolved, name="mark_resolved"),

    #  path('worker-dashboard/', views.worker_dashboard, name='worker_dashboard'),
    # path('mark-resolved/<int:complaint_id>/', views.mark_resolved, name='mark_resolved'),
    # Admin
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("add-worker/", views.add_worker, name="add_worker"),
    path("update-worker/<int:user_id>/", views.update_worker, name="update_worker"),
    path("delete-worker/<int:user_id>/", views.delete_worker, name="delete_worker"),

]
