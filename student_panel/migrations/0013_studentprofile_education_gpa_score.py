
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_panel', '0012_studentprofile_extracurricular_interest_score_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='education_gpa_score',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
