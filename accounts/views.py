from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import DoctorSignUpForm, PatientSignUpForm, DoctorLoginForm, PatientLoginForm
from .models import CustomUser

class LoginGatewayView(TemplateView):
    template_name = 'accounts/login_gateway.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_doctor:
                return redirect('doctor_dashboard')
            elif request.user.is_patient:
                return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class DoctorSignUpView(CreateView):
    model = CustomUser
    form_class = DoctorSignUpForm
    template_name = 'accounts/signup_doctor.html'
    success_url = reverse_lazy('login_doctor')

class PatientSignUpView(CreateView):
    model = CustomUser
    form_class = PatientSignUpForm
    template_name = 'accounts/signup_patient.html'
    success_url = reverse_lazy('login_patient')

class DoctorLoginView(DjangoLoginView):
    form_class = DoctorLoginForm
    template_name = 'accounts/login_doctor.html'
    def get_success_url(self):
        return reverse_lazy('doctor_dashboard')

class PatientLoginView(DjangoLoginView):
    form_class = PatientLoginForm
    template_name = 'accounts/login_patient.html'
    def get_success_url(self):
        return reverse_lazy('home')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard_redirect(request):
    if request.user.is_doctor:
        return redirect('doctor_dashboard')
    elif request.user.is_patient:
        return redirect('home')
    else:
        return redirect('home')
