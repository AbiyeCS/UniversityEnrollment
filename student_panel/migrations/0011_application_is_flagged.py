
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_panel', '0010_chatmessage_applicationnote'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='is_flagged',
            field=models.BooleanField(default=False),
        ),
    ]
