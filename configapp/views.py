from django.shortcuts import render

from .models import (
    HomeProfile, Skill, Project, Experience, Achievement,
    SocialMedia, Contact, Resume, SiteSettings, Language,
)


def home(request):
    return render(request, 'index.html', {
        'profile': HomeProfile.objects.first(),
        'skills': Skill.objects.all(),
        'projects': Project.objects.all(),
        'experiences': Experience.objects.all(),
        'achievements': Achievement.objects.all(),
        'languages': Language.objects.all(),
        'social': SocialMedia.objects.first(),
        'contacts': Contact.objects.first(),
        'resume': Resume.objects.first(),
        'site': SiteSettings.get(),
    })
