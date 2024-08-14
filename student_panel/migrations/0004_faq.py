
import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_panel', '0003_alter_educationalbackground_student_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
            ],
        ),
    ]
