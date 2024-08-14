
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university_panel', '0004_universityprofile_display_image_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='fee',
            field=models.ManyToManyField(blank=True, to='university_panel.fee'),
        ),
    ]
