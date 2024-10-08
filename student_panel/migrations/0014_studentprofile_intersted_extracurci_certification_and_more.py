
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_panel', '0013_studentprofile_education_gpa_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='intersted_extracurci_certification',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='intersted_extracurci_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='intersted_extracurci_name',
            field=models.CharField(choices=[('na', 'NA'), ('painting', 'Painting'), ('writing', 'Writing'), ('debates', 'Debates')], default='na', max_length=50),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='intersted_in_extracurci',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='intersted_in_sports',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='intersted_sport_certification',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='intersted_sport_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='intersted_sport_name',
            field=models.CharField(choices=[('na', 'NA'), ('football', 'FootBall'), ('soccer', 'Soccer'), ('cricket', 'Cricket')], default='na', max_length=50),
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('reviewed', 'Reviewed'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=20),
        ),
    ]
