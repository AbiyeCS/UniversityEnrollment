
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university_panel', '0003_fee_university'),
    ]

    operations = [
        migrations.AddField(
            model_name='universityprofile',
            name='display_image_file',
            field=models.ImageField(blank=True, null=True, upload_to='university_images/'),
        ),
    ]
