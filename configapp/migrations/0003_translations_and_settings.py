from django.db import migrations, models


def copy_legacy_fields(apps, schema_editor):
    """Copy old single-language fields into _en (and mirror to _uz/_ru as fallback)."""
    HomeProfile = apps.get_model('configapp', 'HomeProfile')
    for hp in HomeProfile.objects.all():
        hp.about_me_en = hp.about_me_en or hp.about_me or ''
        hp.about_me_uz = hp.about_me_uz or hp.about_me or ''
        hp.about_me_ru = hp.about_me_ru or hp.about_me or ''
        hp.job_en = hp.job_en or hp.job or 'AI Specialist and Backend Developer'
        hp.job_uz = hp.job_uz or hp.job or 'AI mutaxassis va Backend dasturchi'
        hp.job_ru = hp.job_ru or hp.job or 'AI-специалист и Backend-разработчик'
        if not hp.job:
            hp.job = 'AI Specialist and Backend Developer'
        hp.save()

    Experience = apps.get_model('configapp', 'Experience')
    for e in Experience.objects.all():
        e.project_name_en = e.project_name_en or e.project_name or ''
        e.project_name_uz = e.project_name_uz or e.project_name or ''
        e.project_name_ru = e.project_name_ru or e.project_name or ''
        e.description_en = e.description_en or e.description or ''
        e.description_uz = e.description_uz or e.description or ''
        e.description_ru = e.description_ru or e.description or ''
        e.save()

    Project = apps.get_model('configapp', 'Project')
    for p in Project.objects.all():
        p.name_p_en = p.name_p_en or p.name_p or ''
        p.name_p_uz = p.name_p_uz or p.name_p or ''
        p.name_p_ru = p.name_p_ru or p.name_p or ''
        p.work_description_en = p.work_description_en or p.work_description or ''
        p.work_description_uz = p.work_description_uz or p.work_description or ''
        p.work_description_ru = p.work_description_ru or p.work_description or ''
        p.save()

    Achievement = apps.get_model('configapp', 'Achievement')
    for a in Achievement.objects.all():
        a.name_a_en = a.name_a_en or a.name_a or ''
        a.name_a_uz = a.name_a_uz or a.name_a or ''
        a.name_a_ru = a.name_a_ru or a.name_a or ''
        a.description_en = a.description_en or a.description or ''
        a.description_uz = a.description_uz or a.description or ''
        a.description_ru = a.description_ru or a.description or ''
        a.save()

    Contact = apps.get_model('configapp', 'Contact')
    for c in Contact.objects.all():
        c.location_en = c.location_en or c.location or ''
        c.location_uz = c.location_uz or c.location or ''
        c.location_ru = c.location_ru or c.location or ''
        c.save()


def reverse_noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0002_resume'),
    ]

    operations = [
        # ---- HomeProfile ----
        migrations.AlterField(
            model_name='homeprofile',
            name='job',
            field=models.CharField(default='AI Specialist and Backend Developer', max_length=64),
        ),
        migrations.AddField(
            model_name='homeprofile',
            name='job_uz',
            field=models.CharField(blank=True, default='AI mutaxassis va Backend dasturchi', max_length=64),
        ),
        migrations.AddField(
            model_name='homeprofile',
            name='job_ru',
            field=models.CharField(blank=True, default='AI-специалист и Backend-разработчик', max_length=64),
        ),
        migrations.AddField(
            model_name='homeprofile',
            name='job_en',
            field=models.CharField(blank=True, default='AI Specialist and Backend Developer', max_length=64),
        ),
        migrations.AddField(
            model_name='homeprofile',
            name='about_me_uz',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='homeprofile',
            name='about_me_ru',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='homeprofile',
            name='about_me_en',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='homeprofile',
            name='projects',
            field=models.CharField(blank=True, default='', max_length=32),
        ),

        # ---- Experience ----
        migrations.AddField(
            model_name='experience',
            name='project_name_uz',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='experience',
            name='project_name_ru',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='experience',
            name='project_name_en',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='experience',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='experience',
            name='description_uz',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='experience',
            name='description_ru',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='experience',
            name='description_en',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='experience',
            name='order',
            field=models.IntegerField(default=0, help_text='Lower number = appears first'),
        ),
        migrations.AlterModelOptions(
            name='experience',
            options={'ordering': ['order', '-start_date']},
        ),

        # ---- Skill ----
        migrations.AlterField(
            model_name='skill',
            name='section',
            field=models.CharField(
                choices=[
                    ('BACKEND_DEVELOPMENT', 'Backend Development'),
                    ('DEVOPS_AND_CLOUDING', 'DevOps and Cloud'),
                    ('AI_AND_MACHINELEARNING', 'AI and Machine Learning'),
                    ('DATA_AND_FRONTEND', 'Data and Frontend'),
                ],
                default='BACKEND_DEVELOPMENT',
                max_length=32,
            ),
        ),

        # ---- Achievement ----
        migrations.AddField(
            model_name='achievement',
            name='name_a_uz',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='achievement',
            name='name_a_ru',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='achievement',
            name='name_a_en',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='achievement',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='achievement',
            name='description_uz',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='achievement',
            name='description_ru',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='achievement',
            name='description_en',
            field=models.TextField(blank=True, default=''),
        ),

        # ---- Project ----
        migrations.AddField(
            model_name='project',
            name='name_p_uz',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='project',
            name='name_p_ru',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='project',
            name='name_p_en',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='project',
            name='work_description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='project',
            name='work_description_uz',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='project',
            name='work_description_ru',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='project',
            name='work_description_en',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='project',
            name='technologies',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='project',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['order', 'id']},
        ),

        # ---- Contact ----
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='contact',
            name='location',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='contact',
            name='location_uz',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='contact',
            name='location_ru',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='contact',
            name='location_en',
            field=models.CharField(blank=True, default='', max_length=100),
        ),

        # ---- SocialMedia ----
        migrations.AlterField(
            model_name='socialmedia',
            name='github',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='socialmedia',
            name='instagram',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='socialmedia',
            name='telegram',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='socialmedia',
            name='linkedin',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterModelOptions(
            name='socialmedia',
            options={'verbose_name': 'Social media', 'verbose_name_plural': 'Social media'},
        ),
        migrations.AlterModelOptions(
            name='homeprofile',
            options={'verbose_name': 'Home profile', 'verbose_name_plural': 'Home profile'},
        ),

        # ---- SiteSettings (new) ----
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('footer_signature', models.CharField(default='Powered by Nazarbek', max_length=80)),
                ('background_music', models.FileField(blank=True, null=True, upload_to='music/',
                                                      help_text='Optional quiet background track (mp3/ogg).')),
                ('music_volume', models.FloatField(default=0.18, help_text='0.0 – 1.0 (quiet by default)')),
                ('admin_trigger_word', models.CharField(default='safarov2', max_length=40,
                                                        help_text='Type this anywhere on the site to open admin panel.')),
            ],
            options={
                'verbose_name': 'Site settings',
                'verbose_name_plural': 'Site settings',
            },
        ),

        # ---- Data copy ----
        migrations.RunPython(copy_legacy_fields, reverse_noop),
    ]
