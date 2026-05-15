from django.contrib import admin
from .models import (
    HomeProfile, Experience, Skill, Achievement,
    Project, Contact, SocialMedia, Resume, SiteSettings, Language,
)


@admin.register(HomeProfile)
class HomeProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Job title (3 languages)', {'fields': ('job_en', 'job_uz', 'job_ru', 'job')}),
        ('About me (3 languages)', {'fields': ('about_me_en', 'about_me_uz', 'about_me_ru', 'about_me')}),
        ('Other', {'fields': ('projects',)}),
    )


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('project_name_en', 'start_date', 'end_date', 'order')
    list_editable = ('order',)
    fieldsets = (
        ('Project name (3 languages)', {
            'fields': ('project_name_en', 'project_name_uz', 'project_name_ru', 'project_name')
        }),
        ('Description (3 languages)', {
            'fields': ('description_en', 'description_uz', 'description_ru', 'description')
        }),
        ('Timeline', {'fields': ('start_date', 'end_date', 'order')}),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('skill_name', 'section')
    list_filter = ('section',)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name_a_en', 'photo', 'pdf_file')
    fieldsets = (
        ('Name (3 languages)', {'fields': ('name_a_en', 'name_a_uz', 'name_a_ru', 'name_a')}),
        ('Description (3 languages)', {
            'fields': ('description_en', 'description_uz', 'description_ru', 'description')
        }),
        ('Files', {'fields': ('photo', 'pdf_file')}),
    )


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'level_en', 'flag', 'order')
    list_editable = ('order',)
    fieldsets = (
        ('Name (3 languages)', {'fields': ('name_en', 'name_uz', 'name_ru', 'name')}),
        ('Level (3 languages)', {'fields': ('level_en', 'level_uz', 'level_ru', 'level')}),
        ('Display', {'fields': ('flag', 'order')}),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name_p_en', 'technologies', 'order')
    list_editable = ('order',)
    fieldsets = (
        ('Name (3 languages)', {'fields': ('name_p_en', 'name_p_uz', 'name_p_ru', 'name_p')}),
        ('Description (3 languages)', {
            'fields': ('work_description_en', 'work_description_uz', 'work_description_ru', 'work_description')
        }),
        ('Other', {'fields': ('technologies', 'order')}),
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Contact info', {'fields': ('email', 'phone')}),
        ('Location (3 languages)', {
            'fields': ('location_en', 'location_uz', 'location_ru', 'location')
        }),
    )


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    fields = ('github', 'linkedin', 'telegram', 'instagram')


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('id', 'file')


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fields = ('footer_signature',)

    def has_add_permission(self, request):
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)
