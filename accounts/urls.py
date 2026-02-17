from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginGatewayView.as_view(), name='login'),
    path('signup/doctor/', views.DoctorSignUpView.as_view(), name='signup_doctor'),
    path('signup/patient/', views.PatientSignUpView.as_view(), name='signup_patient'),
    path('login/doctor/', views.DoctorLoginView.as_view(), name='login_doctor'),
    path('login/patient/', views.PatientLoginView.as_view(), name='login_patient'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
]
