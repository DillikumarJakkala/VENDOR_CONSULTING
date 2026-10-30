from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard_root'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('submit/<int:requirement_id>/', views.submit_candidate, name='submit_candidate'),
    path('update-status/<int:candidate_id>/', views.update_candidate_status, name='update_candidate_status'),
]