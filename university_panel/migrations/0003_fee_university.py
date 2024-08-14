
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('university_panel', '0002_alter_course_taught_language_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fee',
            name='university',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='university_panel.universityprofile'),
        ),
    ]
