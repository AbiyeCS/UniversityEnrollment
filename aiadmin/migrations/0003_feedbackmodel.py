
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aiadmin', '0002_alter_trainingmodel_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedbackModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gpa_score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('sports_interest_score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('extracurricular_interest_score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('uni_gpa_weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('uni_sports_weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('uni_extracurricular_weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('accepted', models.IntegerField(default=0)),
            ],
        ),
    ]
