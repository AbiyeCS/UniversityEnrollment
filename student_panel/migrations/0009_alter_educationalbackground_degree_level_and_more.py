
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_panel', '0008_educationalbackground_main_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educationalbackground',
            name='degree_level',
            field=models.CharField(blank=True, choices=[('associate', 'associate'), ('bachelors', 'Bachelors'), ('masters', 'Masters'), ('doctoral', 'Doctoral')], default='associate', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='educationalbackground',
            name='degree_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
