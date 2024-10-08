
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_panel', '0011_application_is_flagged'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='extracurricular_interest_score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='sports_interest_score',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
