
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university_panel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='taught_language',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='university_course_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='universityprofile',
            name='display_image',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='universityprofile',
            name='site_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
