

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from pdfkit import pdfkit

from .forms import *

def home(request):
    profile = HomeProfile.objects.first()
    skills = Skill.objects.all()
    projects = Project.objects.all()
    experiences = Experience.objects.all()
    achievements = Achievement.objects.all()
    social = SocialMedia.objects.first()
    contacts = Contact.objects.first()
    resume = Resume.objects.first()  # ← shu qatorni qo'shing

    return render(request, 'index.html', {
        'profile': profile,
        'skills': skills,
        'projects': projects,
        'experiences': experiences,
        'achievements': achievements,
        'social': social,
        'contacts': contacts,
        'resume': resume,  # ← shu qatorni qo'shing
    })