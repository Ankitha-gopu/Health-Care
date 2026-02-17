from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from appointments.models import Speciality, DoctorProfile

class Command(BaseCommand):
    help = 'Seeds initial data for the healthcare platform'

    def handle(self, *args, **kwargs):
        # Create Specialities
        specialities_data = [
            {'name': 'Pediatrician', 'icon': 'bi-baby'},
            {'name': 'General Physician', 'icon': 'bi-clipboard2-pulse'},
            {'name': 'Gynaecologist', 'icon': 'bi-person-heart'},
            {'name': 'Dermatologist', 'icon': 'bi-droplet'},
            {'name': 'Dietitian', 'icon': 'bi-apple'},
            {'name': 'Orthopedician', 'icon': 'bi-bone'},
            {'name': 'Fertility Specialist', 'icon': 'bi-gender-female'},
            {'name': 'Cardiologist', 'icon': 'bi-heart-pulse'},
            {'name': 'General Surgeon', 'icon': 'bi-scissors'},
            {'name': 'Gastroenterologist', 'icon': 'bi-virus'},
            {'name': 'Pulmonologist', 'icon': 'bi-wind'},
            {'name': 'Oncologist', 'icon': 'bi-shield-pulse'},
        ]

        for data in specialities_data:
            Speciality.objects.update_or_create(name=data['name'], defaults={'icon': data['icon']})

        # Helper to create doctors
        def create_doctor(username, first, last, spec_name, bio, exp, fee, hospital, rating, stories, image):
            user, created = CustomUser.objects.get_or_create(username=username)
            user.first_name = first
            user.last_name = last
            user.email = f'{username}@example.com'
            if created:
                user.set_password('password123')
            user.is_doctor = True
            user.save()

            try:
                spec = Speciality.objects.get(name=spec_name)
            except Speciality.DoesNotExist:
                spec = Speciality.objects.create(name=spec_name, icon='bi-person-badge')

            DoctorProfile.objects.update_or_create(
                user=user,
                defaults={
                    'speciality': spec,
                    'bio': bio,
                    'experience': exp,
                    'consultation_fee': fee,
                    'hospital_name': hospital,
                    'rating': rating,
                    'patient_stories_count': stories,
                    'image_url': image
                }
            )
            self.stdout.write(self.style.SUCCESS(f'Seeded/Updated {username}'))

        create_doctor('dr_ankitha', 'Ankitha', 'Reddy', 'Dermatologist', 'MBBS, MD - DVL', 12, 299, 'Venkat Center for Aesthetic Health, Bengaluru', 4.8, 156, 'https://images.unsplash.com/photo-1559839734-2b71f1e3c77b?auto=format&fit=crop&q=80&w=200')
        create_doctor('dr_harsha', 'Harsha', 'Vardhan', 'General Physician', 'MBBS, DNB - General Medicine', 15, 399, 'City Hospital, Hyderabad', 4.5, 230, 'https://images.unsplash.com/photo-1612349317150-e413f6a5b1a8?auto=format&fit=crop&q=80&w=200')
        create_doctor('dr_jyothi', 'Jyothi', 'Netha', 'Dermatologist', 'MBBS, DDVL - Dermatology', 11, 499, 'Netha Skin Clinic, Bengaluru', 4.7, 85, 'https://images.unsplash.com/photo-1594824476967-48c8b964273f?auto=format&fit=crop&q=80&w=200')
        create_doctor('dr_akshitha', 'Akshitha', 'Reddy', 'Pediatrician', 'MBBS, MD - Pediatrics', 8, 350, 'Kids Care Clinic, Mumbai', 4.6, 112, 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&q=80&w=200')
        create_doctor('dr_samatha', 'Samatha', 'Rao', 'Gynaecologist', 'MBBS, DGO - Gynaecology', 10, 450, 'Women Wellness Center, Pune', 4.5, 90, 'https://images.unsplash.com/photo-1651008376811-b90baee60c1f?auto=format&fit=crop&q=80&w=200')
        create_doctor('dr_triveni', 'Triveni', 'Reddy', 'Cardiologist', 'MBBS, MD, DM - Cardiology', 18, 599, 'Apollo Hospital, Delhi', 4.9, 340, 'https://images.unsplash.com/photo-1527613426441-4da17471b66d?auto=format&fit=crop&q=80&w=200')
        create_doctor('dr_anita', 'Anita', 'Desai', 'Gynaecologist', 'Women Heath & Fertility', 15, 450, 'Lifeline Hospital, Pune', 4.7, 85, 'https://images.unsplash.com/photo-1550831107-1553da8c8464?auto=format&fit=crop&q=80&w=200')
        create_doctor('dr_rahul', 'Rahul', 'Verma', 'Cardiologist', 'Heart Surgery Specialist', 18, 599, 'Apollo Hospital, Delhi', 4.6, 230, 'https://images.unsplash.com/photo-1537368910025-700350fe46c7?auto=format&fit=crop&q=80&w=200')
        create_doctor('dr_chintan', 'Chintan', 'Solanki', 'General Surgeon', 'MBBS, MS - General Surgery', 15, 399, 'Solanki Multispeciality, Ahmedabad', 4.5, 120, 'https://images.unsplash.com/photo-1582750433449-648ed127bb54?auto=format&fit=crop&q=80&w=200')
        create_doctor('dr_suresh', 'Suresh', 'Rao', 'Orthopedician', 'Joint Replacement Surgeon', 22, 550, 'Bone & Joint Clinic, Chennai', 4.4, 45, 'https://images.unsplash.com/photo-1537368910025-700350fe46c7?auto=format&fit=crop&q=80&w=200')
        create_doctor('dr_vikram', 'Vikram', 'Singh', 'Gastroenterologist', 'Digestive Health Expert', 12, 499, 'Relief Clinic, Jaipur', 4.3, 34, 'https://images.unsplash.com/photo-1643297654416-05795d62e39c?auto=format&fit=crop&q=80&w=200')

        # Create a Demo Patient
        if not CustomUser.objects.filter(username='patient_demo').exists():
            CustomUser.objects.create_user(
                username='patient_demo',
                email='patient@example.com',
                password='password123',
                first_name='Ankitha',
                last_name='Gopu',
                is_patient=True
            )
            self.stdout.write(self.style.SUCCESS('Successfully seeded demo patient'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded specialities'))
