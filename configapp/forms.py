from django import forms
from .models import *

class HomeProfileForm(forms.ModelForm):
    class Meta:
        model = HomeProfile
        fields = '__all__'


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = '__all__'


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'


class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = '__all__'


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class SocialMediaForm(forms.ModelForm):
    class Meta:
        model = SocialMedia
        fields = '__all__'