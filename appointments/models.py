from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class Speciality(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='bi-heart-pulse') # Bootstrap icon class
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class DoctorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile')
    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True)
    bio = models.TextField()
    experience = models.PositiveIntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=499.00)
    hospital_name = models.CharField(max_length=200, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    patient_stories_count = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='doctors/', default='default_doctor.png')

    def __str__(self):
        return f"Dr. {self.user.get_full_name() or self.user.username}"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='doctor_appointments')
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    
    # New Patient Details for Consultation
    patient_name = models.CharField(max_length=200, blank=True, null=True)
    patient_age = models.PositiveIntegerField(blank=True, null=True)
    patient_gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)
    patient_phone = models.CharField(max_length=20, blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    
    date = models.DateField()
    time_slot = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    google_meet_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'date', 'time_slot')

    def __str__(self):
        return f"{self.patient.username} with {self.doctor} on {self.date} at {self.time_slot}"

    @property
    def is_past(self):
        appointment_datetime = timezone.make_aware(timezone.datetime.combine(self.date, self.time_slot))
        return appointment_datetime < timezone.now()
