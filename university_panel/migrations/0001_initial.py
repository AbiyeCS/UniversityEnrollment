
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='UniversityProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('display_image', models.CharField(blank=True, null=True, max_length=255)),
                ('site_url', models.CharField(blank=True, null=True, max_length=255)),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='authentication.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='UniversitySession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('application_deadline', models.DateField()),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='university_panel.universityprofile')),
            ],
        ),
        migrations.CreateModel(
            name='UniversityQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='university_panel.universityprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('short_description', models.TextField()),
                ('requirements', models.TextField(blank=True, null=True)),
                ('university_course_url', models.CharField(blank=True, null=True, max_length=255)),
                ('taught_language', models.CharField(blank=True, null=True, max_length=255)),
                ('discipline', models.ManyToManyField(to='university_panel.discipline')),
                ('fee', models.ManyToManyField(to='university_panel.fee')),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='university_panel.universityprofile')),
            ],
        ),
    ]
