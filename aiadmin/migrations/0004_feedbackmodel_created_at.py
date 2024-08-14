
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aiadmin', '0003_feedbackmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackmodel',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
