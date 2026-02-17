from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from .models import Speciality, DoctorProfile, Appointment
import json

@login_required
def chatbot_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').lower()
            
            # Simple AI logic for symptom analysis
            response_data = {
                'message': "I've analyzed your symptoms. Based on what you've described, here is a recommended prescription.",
                'prescription': {
                    'tablets': [],
                    'syrups': [],
                    'diet': "Drink plenty of water, rest well, and eat light, nutritious meals."
                }
            }
            
            # Advanced Symptom Mapping for Exact Prescriptions
            # Advanced Symptom Mapping for Exact Prescriptions
            if any(k in user_message for k in ['cold', 'cough', 'flu', 'throat', 'runny nose']):
                response_data['prescription']['tablets'].append('Levocetirizine 5mg (1 tab at night)')
                response_data['prescription']['syrups'].append('Ascoril D Plus (10ml twice daily)')
                response_data['prescription']['diet'] = "Avoid cold items. Drink warm ginger water and take steam inhalation."
                
            elif any(k in user_message for k in ['fever', 'headache', 'body pain', 'temperature', 'shivering']):
                response_data['prescription']['tablets'].append('Dolo 650mg (1 tab if fever > 100 F)')
                response_data['prescription']['tablets'].append('Pantop 40mg (1 tab before breakfast)')
                response_data['prescription']['diet'] = "Take light food like khichdi or oats. Stay hydrated with plenty of water."

            elif any(k in user_message for k in ['stomach', 'acidity', 'gas', 'burning', 'indigestion', 'pain in stomach']):
                response_data['prescription']['tablets'].append('Pan-D (1 tab before food)')
                response_data['prescription']['syrups'].append('Digene Gel (2 spoon after food)')
                response_data['prescription']['diet'] = "Avoid spicy and oily food. Have curd, buttermilk, and banana."

            elif any(k in user_message for k in ['loose motion', 'diarrhea', 'vomiting', 'stomach upset']):
                response_data['prescription']['tablets'].append('O2 (Ornidazole + Ofloxacin) (1 tab twice daily)')
                response_data['prescription']['diet'] = "Drink ORS frequently. Eat banana, curd rice, and avoid milk."

            elif any(k in user_message for k in ['skin', 'rash', 'itching', 'allergy']):
                response_data['prescription']['tablets'].append('Allegra 120mg (1 tab once daily)')
                response_data['prescription']['syrups'].append('Calamine Lotion (Apply topically)')
                response_data['prescription']['diet'] = "Avoid citrus fruits, spicy food, and keep the skin clean and dry."

            elif any(k in user_message for k in ['eye', 'redness', 'vision', 'itchy eye']):
                response_data['prescription']['syrups'].append('Refresh Tears Eye Drops (1 drop 4 times daily)')
                response_data['prescription']['diet'] = "Reduce screen time, wear sunglasses, and splash cold water frequently."

            elif any(k in user_message for k in ['loose weight', 'weight loss', 'fat', 'lose weight', 'obesity', 'overweight']):
                response_data['message'] = "For weight loss, a combination of calorie deficit and metabolic support is recommended."
                response_data['prescription']['tablets'].append('L-Carnitine 500mg (1 tab before workout)')
                response_data['prescription']['diet'] = "High fiber, low carb diet. Replace sugar with stevia, drink green tea, and include 45 mins of cardio."

            elif any(k in user_message for k in ['gain weight', 'muscle', 'bulk', 'thin', 'underweight']):
                response_data['message'] = "To gain weight healthily, focus on calorie-dense foods and protein synthesis."
                response_data['prescription']['tablets'].append('Protein Supplement (2 scoops with milk)')
                response_data['prescription']['diet'] = "Caloric surplus with healthy fats (ghee, nuts, peanut butter). Include strength training 4 days a week."

            elif any(k in user_message for k in ['energy', 'tired', 'weakness', 'fatigue', 'dizzy']):
                response_data['message'] = "To improve energy levels, focus on micronutrient balance and hydration."
                response_data['prescription']['tablets'].append('Neurobion Forte (1 tab daily after lunch)')
                response_data['prescription']['diet'] = "Eat small, frequent meals. Include dates, soaked almonds, and fresh fruit juices."

            elif any(k in user_message for k in ['hair fall', 'hair loss', 'bald']):
                response_data['message'] = "Hair health depends on vitamins and protein."
                response_data['prescription']['tablets'].append('Biotin 10mg (1 tab daily)')
                response_data['prescription']['syrups'].append('Minoxidil 5% (Apply on scalp at night)')
                response_data['prescription']['diet'] = "Eat eggs, spinach, and nuts. Avoid stress."

            # Universal Fallback
            else:
                response_data['message'] = "I've analyzed your query. To boost your recovery, here is a general health support prescription."
                response_data['prescription']['tablets'].append('A-Z Multivitamin (1 tab after breakfast)')
                response_data['prescription']['diet'] = "Ensure 8 hours of sleep, drink 3L water, and eat a balanced diet rich in proteins and greens."
            
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=405)

# Create your views here.

def home(request):
    specialities = Speciality.objects.all()
    popular_doctors = DoctorProfile.objects.all().order_by('-rating')[:6]
    return render(request, 'appointments/home.html', {
        'specialities': specialities,
        'popular_doctors': popular_doctors
    })

@login_required
def doctor_dashboard(request):
    if not request.user.is_doctor:
        return redirect('home')
    
    # Show only upcoming appointments (today and future)
    today = timezone.now().date()
    appointments = Appointment.objects.filter(
        doctor__user=request.user,
        date__gte=today
    ).order_by('date', 'time_slot')
    
    return render(request, 'appointments/doctor_dashboard.html', {'appointments': appointments})

@login_required
def approve_appointment(request, appointment_id):
    if not request.user.is_doctor:
        return redirect('home')
    
    appointment = Appointment.objects.get(id=appointment_id, doctor__user=request.user)
    appointment.status = 'scheduled'
    appointment.save()
    return redirect('doctor_dashboard')

@login_required
def patient_dashboard(request):
    if not request.user.is_patient:
        return redirect('home')
    appointments = Appointment.objects.filter(patient=request.user).order_by('date', 'time_slot')
    return render(request, 'appointments/patient_dashboard.html', {'appointments': appointments})

@login_required
def update_meet_link(request, appointment_id):
    if not request.user.is_doctor:
        return redirect('home')
    appointment = Appointment.objects.get(id=appointment_id, doctor__user=request.user)
    if request.method == 'POST':
        link = request.POST.get('meet_link')
        appointment.google_meet_link = link
        appointment.status = 'in_progress' if link else 'scheduled'
        appointment.save()
    return redirect('doctor_dashboard')

def doctor_list(request, speciality_id):
    speciality = Speciality.objects.get(id=speciality_id)
    doctors = DoctorProfile.objects.filter(speciality=speciality)
    return render(request, 'appointments/doctor_list.html', {'speciality': speciality, 'doctors': doctors})

@login_required
def consultation_step1(request):
    if request.method == 'POST':
        request.session['consultation_data'] = {
            'patient_name': request.POST.get('patient_name'),
            'patient_age': request.POST.get('patient_age'),
            'patient_gender': request.POST.get('patient_gender'),
            'patient_phone': request.POST.get('patient_phone'),
            'symptoms': request.POST.get('symptoms'),
        }
        
        doctor_id = request.session.get('selected_doctor_id')
        if doctor_id:
            doctor = DoctorProfile.objects.get(id=doctor_id)
            return redirect('consultation_step3', speciality_id=doctor.speciality.id)
            
        return redirect('consultation_step2')
    return render(request, 'appointments/consultation_step1.html', {'range_100': range(1, 101)})

@login_required
def consultation_step2(request):
    specialities = Speciality.objects.all()
    return render(request, 'appointments/consultation_step2.html', {'specialities': specialities})

@login_required
def consultation_step3(request, speciality_id):
    speciality = Speciality.objects.get(id=speciality_id)
    return render(request, 'appointments/consultation_triage.html', {'speciality': speciality})

@login_required
def consultation_date_time(request, speciality_id):
    speciality = Speciality.objects.get(id=speciality_id)
    doctor_id = request.session.get('selected_doctor_id')
    
    if request.method == 'POST':
        data = request.session.get('consultation_data', {})
        data['date'] = request.POST.get('consultancy_date') or timezone.now().date().isoformat()
        data['time'] = request.POST.get('consultancy_time') or timezone.now().time().isoformat()
        request.session['consultation_data'] = data
        return redirect('consultation_complete', speciality_id=speciality.id)
    
    # If a specific doctor is selected, we could skip this page and do an "Instant Consult"
    # For now, we allow the user to see the page, but we can make it auto-submit or just show "Consult Now"
    return render(request, 'appointments/select_date_time.html', {
        'speciality': speciality,
        'instant_consult': True if doctor_id else False
    })

@login_required
def consultation_complete(request, speciality_id):
    data = request.session.get('consultation_data', {})
    speciality = Speciality.objects.get(id=speciality_id)
    
    # Logic to assign a doctor (e.g., first available or popular)
    doctor_id = request.session.get('selected_doctor_id')
    if doctor_id:
        doctor = DoctorProfile.objects.get(id=doctor_id)
    else:
        doctor = DoctorProfile.objects.filter(speciality=speciality).order_by('-rating').first()
        
    if not doctor:
        doctor = DoctorProfile.objects.first() # Fallback

    # Create the appointment
    appt = Appointment.objects.create(
        patient=request.user,
        doctor=doctor,
        speciality=speciality,
        patient_name=data.get('patient_name'),
        patient_age=data.get('patient_age'),
        patient_gender=data.get('patient_gender'),
        patient_phone=data.get('patient_phone'),
        symptoms=data.get('symptoms'),
        date=data.get('date') or timezone.now().date(),
        time_slot=data.get('time') or timezone.now().time(),
        status='pending'
    )
    
    # Clear session
    if 'consultation_data' in request.session:
        del request.session['consultation_data']
    if 'selected_doctor_id' in request.session:
        del request.session['selected_doctor_id']
        
    return redirect('patient_dashboard')

@login_required
def consultation_room(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    # Check if user is either the patient or the doctor
    if request.user != appointment.patient and (not hasattr(request.user, 'doctor_profile') or request.user.doctor_profile != appointment.doctor):
        return redirect('dashboard')
    
    return render(request, 'appointments/consultation_room.html', {'appointment': appointment})

@login_required
def book_appointment(request, doctor_id):
    return redirect('initialize_consultation', doctor_id=doctor_id)

@login_required
def initialize_consultation(request, doctor_id):
    doctor = DoctorProfile.objects.get(id=doctor_id)
    request.session['selected_doctor_id'] = doctor_id
    # We also pre-populate speciality if possible
    return redirect('consultation_step1')
