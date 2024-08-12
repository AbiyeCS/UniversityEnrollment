from ckeditor.fields import RichTextField
from authentication.models import *
from university_panel.models import *


class StudentProfile(models.Model):
    SPORTS_NAME = (
        ('na', 'NA'),
        ('football', 'FootBall'),
        ('soccer', 'Soccer'),
        ('cricket', 'Cricket'),
    )
    EXTRA_CURRICULAR = (
        ('na', 'NA'),
        ('painting', 'Painting'),
        ('writing', 'Writing'),
        ('debates', 'Debates'),
    )

    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    educational_background = models.ManyToManyField('EducationalBackground', blank=True)
    education_gpa_score = models.FloatField(null=True, blank=True)
    sports_interest_score = models.FloatField(null=True, blank=True)
    extracurricular_interest_score = models.FloatField(null=True, blank=True)

    interested_in_sports = models.BooleanField(default=False)
    interested_sport_name = models.CharField(choices=SPORTS_NAME, max_length=50, default='na')
    interested_sport_certification = models.BooleanField(default=False)
    interested_sport_description = models.TextField(null=True, blank=True)
    interested_in_extracurci = models.BooleanField(default=False)
    interested_extracurci_name = models.CharField(choices=EXTRA_CURRICULAR, max_length=50, default='na')
    interested_extracurci_certification = models.BooleanField(default=False)
    interested_extracurci_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user_profile.user.username

    def calculate_overall_educational_score(self):
        backgrounds = self.educationalbackground_set.all()
        if not backgrounds:
            return 0
        scores = [bg.calculate_educational_score() for bg in backgrounds]
        overall_score = sum(scores) / len(scores)
        self.education_gpa_score =  overall_score
        self.save(update_fields=['education_gpa_score'])
        return overall_score

    def calculate_sports_interest_score(self):
        score = 0
        if self.interested_in_sports:
            score += 20
        if self.interested_sport_name != 'na':
            score += 20
        if self.interested_sport_certification:
            score += 20
        if self.interested_sport_description:
            score +=20
        self.sports_interest_score = score
        self.save(update_fields=['sports_interest_score'])
        return score

    def calculate_extracurricular_interest_score(self):
        score = 0
        if self.interested_in_extracurci:
            score += 20
        if self.interested_extracurci_name != 'na':
            score += 20
        if self.interested_extracurci_certification:
            score += 20
        if self.interested_extracurci_description:
            score += 20
        self.extracurricular_interest_score = score
        self.save(update_fields=['extracurricular_interest_score'])



class Application(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    university = models.ForeignKey(UniversityProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    personal_statement = models.TextField(null=True, blank=True)

    status = models.CharField(choices=STATUS, max_length=20, default='pending')
    is_flagged = models.BooleanField(default=False)
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user_profile.user.username} - {self.university.name} - {self.course.name}"


class EducationalBackground(models.Model):
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, null=True, blank=True)
    DEGREE_LEVEL_CHOICES = (
        ('associate', 'associate'),
        ('bachelors', 'Bachelors'),
        ('masters', 'Masters'),
        ('doctoral', 'Doctoral'),
    )
    MAIN_DEGREE_LEVEL_CHOICES = (
        ('high_school', 'High School'),
        ('professional_degree', 'Professional Degree'),
    )

    main_type = models.CharField(max_length=100,null=True, blank=True)
    institution_name = models.CharField(max_length=255,null=True, blank=True)
    degree_name = models.CharField(max_length=255, null=True, blank=True)
    degree_level = models.CharField(max_length=255, choices=DEGREE_LEVEL_CHOICES, default='associate',null=True, blank=True)
    total_marks = models.IntegerField(null=True, blank=True)
    obtained_marks = models.IntegerField(null=True, blank=True)
    grade = models.CharField(max_length=1,null=True, blank=True)
    obtained_cgpa = models.FloatField(null=True, blank=True)
    total_cgpa = models.FloatField(null=True, blank=True)
    percentage = models.FloatField(null=True, blank=True)
    attended_from = models.DateField(null=True, blank=True)
    attended_to = models.DateField(null=True, blank=True)
    subject_list = models.ManyToManyField('Subject', blank=True)

    def calculate_educational_score(self):
        GRADE_TO_SCORE = {
            'A': 90,
            'B': 80,
            'C': 70,
            'D': 60,
            'F': 50,
        }
        score = 0

        if self.subject_list.exists():
            total_score = 0
            valid_grades_count = 0

            for subject in self.subject_list.all():
                if subject.grade and subject.grade in GRADE_TO_SCORE:
                    total_score += GRADE_TO_SCORE[subject.grade]
                    valid_grades_count += 1

            if valid_grades_count > 0:
                average_score = total_score / valid_grades_count
                score = average_score
                # Assign the grade based on the average score
                if average_score >= 90:
                    self.grade = 'A'
                elif average_score >= 80:
                    self.grade = 'B'
                elif average_score >= 70:
                    self.grade = 'C'
                elif average_score >= 60:
                    self.grade = 'D'
                else:
                    self.grade = 'F'

        elif self.total_marks and self.obtained_marks:
            if self.total_marks > 0:
                percentage_score = (self.obtained_marks / self.total_marks) * 100
                score = percentage_score

        elif self.total_cgpa and self.obtained_cgpa:
            if self.total_cgpa > 0:
                cgpa_percentage = (self.obtained_cgpa / self.total_cgpa) * 100
                score = cgpa_percentage

        elif self.percentage:
            score = self.percentage

        score = max(0, min(score, 100))
        return score


class Subject(models.Model):
    title = models.CharField(max_length=255)
    element_code = models.CharField(max_length=255, null=True, blank=True)
    grade = models.CharField(max_length=1, null=True,blank=True)



class FAQ(models.Model):
    title = models.CharField(max_length=255,null=True, blank=True)
    section = RichTextField(null=True, blank=True)

    def __str__(self):
        return f"{self.title}"


class ApplicationQA(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()


class ApplicationNote(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    note = models.TextField()


class ChatMessage(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_receiver')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sender')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
