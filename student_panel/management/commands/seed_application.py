from django.core.management.base import BaseCommand
from student_panel.models import StudentProfile, Application
from university_panel.models import UniversityProfile, Course
from django.utils import timezone

class Command(BaseCommand):
    help = 'Create applications for every student for every university'

    def handle(self, *args, **kwargs):
        students = StudentProfile.objects.all()
        universities = UniversityProfile.objects.all()

        if not students.exists():
            self.stdout.write(self.style.ERROR('No students found in the database.'))
            return

        if not universities.exists():
            self.stdout.write(self.style.ERROR('No universities found in the database.'))
            return

        for student in students:
            for university in universities:
                courses = university.course_set.all()
                if not courses.exists():
                    self.stdout.write(self.style.WARNING(f'No courses found for university {university.name}. Creating a default course.'))
                    course = Course.objects.create(
                        university=university,
                        name=f'Default Course for {university.name}',
                        short_description='This is a default course created automatically.'
                    )
                else:
                    course = courses.first()  # You can choose a different selection method if needed

                Application.objects.create(
                    student=student,
                    university=university,
                    course=course,
                    personal_statement=f'This is the personal statement for {student.user_profile.user.username}.',
                    status='pending',
                    is_flagged=False,
                    submission_date=timezone.now()
                )

        print('Successfully created applications for every student for every university')
