from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('student_panel', '0014_studentprofile_intersted_extracurci_certification_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentprofile',
            old_name='intersted_extracurci_certification',
            new_name='interested_extracurci_certification',
        ),
        migrations.RenameField(
            model_name='studentprofile',
            old_name='intersted_extracurci_description',
            new_name='interested_extracurci_description',
        ),
        migrations.RenameField(
            model_name='studentprofile',
            old_name='intersted_extracurci_name',
            new_name='interested_extracurci_name',
        ),
        migrations.RenameField(
            model_name='studentprofile',
            old_name='intersted_in_extracurci',
            new_name='interested_in_extracurci',
        ),
        migrations.RenameField(
            model_name='studentprofile',
            old_name='intersted_in_sports',
            new_name='interested_in_sports',
        ),
        migrations.RenameField(
            model_name='studentprofile',
            old_name='intersted_sport_certification',
            new_name='interested_sport_certification',
        ),
        migrations.RenameField(
            model_name='studentprofile',
            old_name='intersted_sport_description',
            new_name='interested_sport_description',
        ),
        migrations.RenameField(
            model_name='studentprofile',
            old_name='intersted_sport_name',
            new_name='interested_sport_name',
        )
    ]