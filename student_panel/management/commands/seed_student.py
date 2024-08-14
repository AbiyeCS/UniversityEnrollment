from django.core.management.base import BaseCommand
from authentication.models import User, UserProfile
from student_panel.models import StudentProfile, EducationalBackground, Subject
from django.utils import timezone
import random


class Command(BaseCommand):
    help = 'Create 50 students with profiles and educational backgrounds, and add a superuser.'

    def handle(self, *args, **kwargs):
        # Create Superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@local.com',
                password='password123',
                first_name='Admin',
                last_name='User'
            )
            print('Superuser "admin" created successfully.')
        else:
            print('Superuser "admin" already exists.')

        # Create 50 students
        if not User.objects.filter(username='student_1').exists():
            for i in range(1, 51):
                # Create User
                user = User.objects.create_user(
                    username=f'student_{i}',
                    email=f'student_{i}@example.com',
                    password='password123',
                    first_name=f'test_{i}',
                    last_name="last"
                )

                # Create UserProfile
                user_profile = UserProfile.objects.create(
                    user=user,
                    user_type='student'
                )

                # Create StudentProfile
                student_profile = StudentProfile.objects.create(
                    user_profile=user_profile,
                    date_of_birth=timezone.now().date(),
                    address=f'123 Street {i}, City, Country',
                    phone_number=f'+1234567890{i}'
                )

                # Create EducationalBackground
                educational_background = EducationalBackground.objects.create(
                    student_profile=student_profile,
                    institution_name=f'Institution {i}',
                    degree_name=f'Degree {i}',
                    degree_level=random.choice(['associate', 'bachelors', 'masters', 'doctoral']),
                    grade=random.choice(['A', 'B', 'C', 'D', 'F']),
                    attended_from=timezone.now().date(),
                    attended_to=timezone.now().date(),
                )

                # Add subjects to educational background
                for j in range(1, 4):
                    subject = Subject.objects.create(
                        title=f'Subject {j} for student {i}',
                        element_code=f'SUBJ{i}{j}',
                        grade=random.choice(['A', 'B', 'C', 'D', 'F']),
                    )
                    educational_background.subject_list.add(subject)

                educational_background.save()
                student_profile.calculate_overall_educational_score()

                # Assign random scores for sports_interest_score and extracurricular_interest_score
                student_profile.sports_interest_score = random.uniform(0, 100)
                student_profile.extracurricular_interest_score = random.uniform(0, 100)
                student_profile.save(update_fields=['sports_interest_score', 'extracurricular_interest_score'])

            print('Successfully created 50 students with profiles and educational backgrounds')
