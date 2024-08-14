
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('university_panel', '0005_alter_course_fee'),
    ]

    operations = [
        migrations.CreateModel(
            name='UniversityAIWeight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gpa_weight', models.FloatField(default=1.0)),
                ('sports_interest_weight', models.FloatField(default=1.0)),
                ('extracurricular_interest_weight', models.FloatField(default=1.0)),
                ('university_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='university_panel.universityprofile')),
            ],
        ),
    ]
