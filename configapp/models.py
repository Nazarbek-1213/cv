from django.db import models

SKILL_SECTIONS = (
    ('BACKEND_DEVELOPMENT', 'Backend Development'),
    ('DEVOPS_AND_CLOUDING', 'DevOps and Cloud'),
    ('AI_AND_MACHINELEARNING', 'AI and Machine Learning'),
    ('DATA_AND_FRONTEND', 'Data and Frontend'),
)


class HomeProfile(models.Model):
    job = models.CharField(max_length=64, default='AI Specialist and Backend Developer')
    job_uz = models.CharField(max_length=64, default='AI mutaxassis va Backend dasturchi', blank=True)
    job_ru = models.CharField(max_length=64, default='AI-специалист и Backend-разработчик', blank=True)
    job_en = models.CharField(max_length=64, default='AI Specialist and Backend Developer', blank=True)

    about_me = models.TextField(default='')
    about_me_uz = models.TextField(default='', blank=True)
    about_me_ru = models.TextField(default='', blank=True)
    about_me_en = models.TextField(default='', blank=True)

    projects = models.CharField(max_length=32, default='', blank=True)

    class Meta:
        verbose_name = 'Home profile'
        verbose_name_plural = 'Home profile'

    def __str__(self):
        return self.job_en or self.job or 'Home profile'


class Experience(models.Model):
    project_name = models.CharField(max_length=255, default='')
    project_name_uz = models.CharField(max_length=255, default='', blank=True)
    project_name_ru = models.CharField(max_length=255, default='', blank=True)
    project_name_en = models.CharField(max_length=255, default='', blank=True)

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    description = models.TextField(default='', blank=True)
    description_uz = models.TextField(default='', blank=True)
    description_ru = models.TextField(default='', blank=True)
    description_en = models.TextField(default='', blank=True)

    order = models.IntegerField(default=0, help_text='Lower number = appears first')

    class Meta:
        ordering = ['order', '-start_date']

    def __str__(self):
        return self.project_name_en or self.project_name or '(experience)'


class Skill(models.Model):
    skill_name = models.CharField(max_length=40)
    section = models.CharField(max_length=32, choices=SKILL_SECTIONS, default='BACKEND_DEVELOPMENT')

    def __str__(self):
        return self.skill_name


class Achievement(models.Model):
    name_a = models.CharField(max_length=255, null=True, blank=True)
    name_a_uz = models.CharField(max_length=255, blank=True, default='')
    name_a_ru = models.CharField(max_length=255, blank=True, default='')
    name_a_en = models.CharField(max_length=255, blank=True, default='')

    photo = models.ImageField(upload_to='achievements/', null=True, blank=True)
    pdf_file = models.FileField(upload_to='achievements/', null=True, blank=True,
                                help_text='Optional PDF (combined certificate, transcript, etc.)')

    description = models.TextField(default='', blank=True)
    description_uz = models.TextField(default='', blank=True)
    description_ru = models.TextField(default='', blank=True)
    description_en = models.TextField(default='', blank=True)

    def __str__(self):
        return self.name_a_en or self.name_a or '(achievement)'


class Language(models.Model):
    name = models.CharField(max_length=40, default='')
    name_en = models.CharField(max_length=40, default='', blank=True)
    name_uz = models.CharField(max_length=40, default='', blank=True)
    name_ru = models.CharField(max_length=40, default='', blank=True)

    level = models.CharField(max_length=24, default='Fluent', blank=True)
    level_en = models.CharField(max_length=24, default='', blank=True)
    level_uz = models.CharField(max_length=24, default='', blank=True)
    level_ru = models.CharField(max_length=24, default='', blank=True)

    flag = models.CharField(max_length=8, default='', blank=True,
                            help_text='Optional emoji flag, e.g. 🇬🇧')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name_en or self.name or '(language)'


class Project(models.Model):
    name_p = models.CharField(max_length=100, default='')
    name_p_uz = models.CharField(max_length=100, default='', blank=True)
    name_p_ru = models.CharField(max_length=100, default='', blank=True)
    name_p_en = models.CharField(max_length=100, default='', blank=True)

    work_description = models.TextField(default='', blank=True)
    work_description_uz = models.TextField(default='', blank=True)
    work_description_ru = models.TextField(default='', blank=True)
    work_description_en = models.TextField(default='', blank=True)

    technologies = models.CharField(max_length=255, default='', blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name_p_en or self.name_p or '(project)'


class Contact(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20, default='', blank=True)
    location = models.CharField(max_length=100, default='', blank=True)
    location_uz = models.CharField(max_length=100, default='', blank=True)
    location_ru = models.CharField(max_length=100, default='', blank=True)
    location_en = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return self.email


class SocialMedia(models.Model):
    github = models.CharField(max_length=200, default='', blank=True)
    instagram = models.CharField(max_length=200, default='', blank=True)
    telegram = models.CharField(max_length=200, default='', blank=True)
    linkedin = models.CharField(max_length=200, default='', blank=True)

    class Meta:
        verbose_name = 'Social media'
        verbose_name_plural = 'Social media'

    def __str__(self):
        return self.github or self.linkedin or '(social)'


class Resume(models.Model):
    file = models.FileField(upload_to='resume/')

    def __str__(self):
        return self.file.name if self.file else '(resume)'


class SiteSettings(models.Model):
    """Singleton-style settings. Only the footer signature is exposed publicly.

    The secret admin entry is a hidden button at the footer signature itself
    (triple-click or 1.5s long-press), so no trigger-word setting is needed.
    """
    footer_signature = models.CharField(max_length=80, default='Powered by Nazarbek')

    class Meta:
        verbose_name = 'Site settings'
        verbose_name_plural = 'Site settings'

    def __str__(self):
        return 'Site settings'

    @classmethod
    def get(cls):
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create()
        return obj
