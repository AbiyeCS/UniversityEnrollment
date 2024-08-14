
import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student_panel', '0005_faq_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='section',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
