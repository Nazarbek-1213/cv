from django.db import models

SKILL_SECTIONS = (
    ('BACKEND_DEVELOPMENT', 'Backend Development'),
    ('DEVOPS_AND_CLOUDING', 'DevOps and Cloud'),
    ('AI_AND_MACHINELEARNING', 'AI and Machine Learning'),
    ('DATA_AND_FRONTEND', 'Data and Frontend'),
)


class HomeProfile(models.Model):
    about_me = models.TextField(default='')
    job = models.CharField(max_length=32, default='')
    projects = models.CharField(max_length=32, default='')

    def __str__(self):
        return self.job


class Experience(models.Model):
    project_name = models.CharField(max_length=255, default='')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.project_name


class Skill(models.Model):
    skill_name = models.CharField(max_length=40)
    section = models.CharField(max_length=32, choices=SKILL_SECTIONS)

    def __str__(self):
        return self.skill_name


class Achievement(models.Model):
    name_a = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(upload_to='achievements/', null=True, blank=True)
    description = models.TextField(default='')

    def __str__(self):
        return self.name_a or ''


class Project(models.Model):
    name_p = models.CharField(max_length=100, default='')
    work_description = models.TextField(default='')
    technologies = models.CharField(max_length=255, default='')  # typo fixed

    def __str__(self):
        return self.name_p


class Contact(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20, default='')
    location = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.email


class SocialMedia(models.Model):
    github = models.CharField(max_length=100, default='')
    instagram = models.CharField(max_length=100, default='')
    telegram = models.CharField(max_length=100, default='')
    linkedin = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.instagram

class Resume(models.Model):
    file = models.FileField(upload_to='resume/')