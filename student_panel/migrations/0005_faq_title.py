
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_panel', '0004_faq'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
