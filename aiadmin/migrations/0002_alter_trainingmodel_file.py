
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aiadmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainingmodel',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='training_files/'),
        ),
    ]
