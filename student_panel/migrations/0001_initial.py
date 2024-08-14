
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('university_panel', '0001_initial'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personal_statement', models.TextField(blank=True, null=True)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='university_panel.course')),
            ],
        ),
        migrations.CreateModel(
            name='EducationalBackground',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree_name', models.CharField(max_length=255)),
                ('degree_level', models.CharField(choices=[('associate', 'associate'), ('bachelors', 'Bachelors'), ('masters', 'Masters'), ('doctoral', 'Doctoral')], default='associate', max_length=255)),
                ('total_marks', models.IntegerField(blank=True, null=True)),
                ('obtained_marks', models.IntegerField(blank=True, null=True)),
                ('grade', models.CharField(blank=True, max_length=1, null=True)),
                ('obtained_cgpa', models.FloatField(blank=True, null=True)),
                ('total_cgpa', models.FloatField(blank=True, null=True)),
                ('percentage', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('educational_background', models.ManyToManyField(to='student_panel.educationalbackground')),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='authentication.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationQA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_panel.application')),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_panel.studentprofile'),
        ),
        migrations.AddField(
            model_name='application',
            name='university',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='university_panel.universityprofile'),
        ),
    ]
