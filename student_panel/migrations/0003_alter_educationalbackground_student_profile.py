
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_panel', '0002_educationalbackground_student_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educationalbackground',
            name='student_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_panel.studentprofile'),
        ),
    ]
