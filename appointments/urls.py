from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('approve-appointment/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),
    path('update-meet-link/<int:appointment_id>/', views.update_meet_link, name='update_meet_link'),
    path('speciality/<int:speciality_id>/', views.doctor_list, name='doctor_list'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('consult/step1/', views.consultation_step1, name='consultation_step1'),
    path('consult/step2/', views.consultation_step2, name='consultation_step2'),
    path('consult/step3/spec/<int:speciality_id>/', views.consultation_step3, name='consultation_step3'),
    path('consult/date-time/<int:speciality_id>/', views.consultation_date_time, name='consultation_date_time'),
    path('consult/complete/<int:speciality_id>/', views.consultation_complete, name='consultation_complete'),
    path('consultation/room/<int:appointment_id>/', views.consultation_room, name='consultation_room'),
    path('consult/init/<int:doctor_id>/', views.initialize_consultation, name='initialize_consultation'),
    path('api/chatbot-response/', views.chatbot_response, name='chatbot_response'),
] # Force reload comment
