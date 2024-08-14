
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_panel', '0006_alter_faq_section'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('element_code', models.CharField(blank=True, max_length=255, null=True)),
                ('grade', models.CharField(blank=True, max_length=1, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='educationalbackground',
            name='attended_from',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='educationalbackground',
            name='attended_to',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='educationalbackground',
            name='institution_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='educational_background',
            field=models.ManyToManyField(blank=True, to='student_panel.educationalbackground'),
        ),
        migrations.AddField(
            model_name='educationalbackground',
            name='subject_list',
            field=models.ManyToManyField(blank=True, to='student_panel.subject'),
        ),
    ]
