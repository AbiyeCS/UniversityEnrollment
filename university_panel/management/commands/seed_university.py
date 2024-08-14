import random
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from django.contrib.auth.models import User
from authentication.models import UserProfile
from university_panel.models import UniversityProfile, UniversitySession, Discipline, Course, Fee, UniversityAIWeight

class Command(BaseCommand):
    help = 'Seed the database with demo data'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        if self.check_existing_users():
            self.stdout.write(self.style.ERROR('User(s) with the same username already exist. Stopping the seeding process.'))
            return

        self.seed_disciplines()
        self.seed_universities()
        self.seed_courses()
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database'))

    def check_existing_users(self):
        """Check if any users with the same username already exist."""
        usernames = [f'dummyuser{i}' for i in range(10)]
        existing_users = User.objects.filter(username__in=usernames)
        return existing_users.exists()

    def seed_disciplines(self):
        disciplines = ['Computer Science', 'Business Administration', 'Mechanical Engineering',
                       'Electrical Engineering', 'Civil Engineering', 'Medicine', 'Law', 'Physics',
                       'Mathematics', 'Chemistry']
        for discipline_name in disciplines:
            Discipline.objects.create(name=discipline_name)
        self.stdout.write(self.style.SUCCESS('Seeded Disciplines'))

    def seed_universities(self):
        university_names = [
            'Harvard University', 'Stanford University', 'MIT', 'University of Cambridge',
            'University of Oxford', 'Caltech', 'University of Chicago', 'Imperial College London',
            'ETH Zurich', 'University College London'
        ]
        addresses = [
            'Cambridge, MA', 'Stanford, CA', 'Cambridge, MA', 'Cambridge, UK',
            'Oxford, UK', 'Pasadena, CA', 'Chicago, IL', 'London, UK',
            'Zurich, Switzerland', 'London, UK'
        ]
        image_urls = [
            'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Harvard_University_coat_of_arms.svg/300px-Harvard_University_coat_of_arms.svg.png',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Seal_of_Leland_Stanford_Junior_University.svg/300px-Seal_of_Leland_Stanford_Junior_University.svg.png',
            'https://upload.wikimedia.org/wikipedia/en/thumb/4/44/MIT_Seal.svg/300px-MIT_Seal.svg.png',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Coat_of_Arms_of_the_University_of_Cambridge.svg/150px-Coat_of_Arms_of_the_University_of_Cambridge.svg.png',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Arms_of_University_of_Oxford.svg/300px-Arms_of_University_of_Oxford.svg.png',
            'https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/Seal_of_the_California_Institute_of_Technology.svg/300px-Seal_of_the_California_Institute_of_Technology.svg.png',
            'https://upload.wikimedia.org/wikipedia/en/thumb/7/79/University_of_Chicago_shield.svg/260px-University_of_Chicago_shield.svg.png',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Shield_of_Imperial_College_London.svg/260px-Shield_of_Imperial_College_London.svg.png',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/ETH_Z%C3%BCrich_im_Abendlicht.jpg/440px-ETH_Z%C3%BCrich_im_Abendlicht.jpg',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Wilkins_Building_1%2C_UCL%2C_London_-_Diliff.jpg/400px-Wilkins_Building_1%2C_UCL%2C_London_-_Diliff.jpg'
        ]
        site_urls = [
            'https://www.harvard.edu', 'https://www.stanford.edu', 'https://www.mit.edu',
            'https://www.cam.ac.uk', 'https://www.ox.ac.uk', 'https://www.caltech.edu',
            'https://www.uchicago.edu', 'https://www.imperial.ac.uk', 'https://www.ethz.ch',
            'https://www.ucl.ac.uk'
        ]

        for i in range(10):
            # Create a new user and user profile for each university
            user = User.objects.create_user(username=f'dummyuser{i}', password='dummyuserpassword')
            user_profile = UserProfile.objects.create(user=user, user_type='university')

            university = UniversityProfile.objects.create(
                user_profile=user_profile,
                name=university_names[i],
                address=addresses[i],
                display_image=image_urls[i],
                site_url=site_urls[i]
            )
            UniversitySession.objects.create(
                university=university,
                start_date='2024-09-01',
                application_deadline='2024-07-31'
            )

            # Randomly assign weights that sum up to 100
            weights = self.generate_weights()
            UniversityAIWeight.objects.create(
                university_profile=university,
                gpa_weight=weights[0],
                sports_interest_weight=weights[1],
                extracurricular_interest_weight=weights[2]
            )

        self.stdout.write(self.style.SUCCESS('Seeded Universities'))

    def generate_weights(self):
        # Generate two random cut points between 1 and 99
        a = random.randint(1, 99)
        b = random.randint(1, 99)

        x, y = sorted([a, b])

        weight1 = x
        weight2 = y - x
        weight3 = 100 - y
        return [weight1, weight2, weight3]

    def seed_courses(self):
        course_names = [
            'Introduction to Computer Science', 'Advanced Business Strategy', 'Thermodynamics',
            'Circuit Analysis', 'Structural Engineering', 'Human Anatomy', 'Constitutional Law',
            'Quantum Mechanics', 'Linear Algebra', 'Organic Chemistry',
            'Data Structures', 'Financial Accounting', 'Fluid Mechanics',
            'Digital Signal Processing', 'Geotechnical Engineering', 'Pathology',
            'Criminal Law', 'Statistical Physics', 'Calculus', 'Physical Chemistry'
        ]
        short_descriptions = [
            'An introduction to the basics of computer science.', 'Strategic management and business policy.',
            'The principles of thermodynamics and heat transfer.', 'Analysis of electrical circuits.',
            'The fundamentals of structural analysis and design.', 'The structure and function of the human body.',
            'An overview of constitutional law principles.', 'The fundamentals of quantum mechanics.',
            'An introduction to linear algebra concepts.', 'The study of organic chemical compounds.',
            'Data organization and management in computer science.', 'The basics of financial accounting.',
            'The study of fluid behavior.', 'Digital signal processing techniques and applications.',
            'The principles of soil mechanics and foundation design.', 'The study of diseases and their effects.',
            'An overview of criminal law principles.', 'The fundamentals of statistical mechanics.',
            'An introduction to differential and integral calculus.', 'The study of physical properties of chemicals.'
        ]
        disciplines = list(Discipline.objects.all())
        for i in range(20):
            course = Course.objects.create(
                university=UniversityProfile.objects.order_by('?').first(),
                name=course_names[i],
                short_description=short_descriptions[i],
                requirements='Requirements for the course.',
                university_course_url='https://example.com/course-url',
                taught_language='English'
            )
            course.discipline.set(random.sample(disciplines, k=2))
            for fee_name, fee_amount in [('Tuition Fee', 10000.00), ('Lab Fee', 500.00)]:
                fee = Fee.objects.create(name=fee_name, amount=fee_amount)
                course.fee.add(fee)
        self.stdout.write(self.style.SUCCESS('Seeded Courses'))
