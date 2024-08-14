
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_panel', '0007_subject_educationalbackground_attended_from_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='educationalbackground',
            name='main_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
