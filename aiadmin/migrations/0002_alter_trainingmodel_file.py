# Generated by Django 4.2 on 2024-08-03 16:32

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
