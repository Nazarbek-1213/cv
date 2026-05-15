"""Idempotent seed/cleanup for the CV site.

What this command does on every run:
  * Removes any Experience / Project entries whose name does NOT contain
    'kinofond' (case-insensitive). The mini-OLX placeholder and similar
    leftovers are wiped here.
  * Deduplicates KinoFond entries to exactly one Experience + one Project.
  * Refreshes the KinoFond Experience (Mar 2026 -> present) with the full
    description in 3 languages.
  * Ensures Technical Arsenal contains both the general stack and the
    KinoFond-specific tech (HTML5 video streaming, HTTP Range, email OTP,
    X-Accel-Redirect, etc.) — no duplicates.
  * Back-fills `_uz` / `_ru` / `_en` fields from the legacy single-language
    field on every row, so old data is multilingual-ready.
  * Sets a default Contact / Social row only when none exist.
  * Ensures a single SiteSettings row with `Powered by Nazarbek`.
"""
from datetime import date

from django.core.management.base import BaseCommand

from configapp.models import (
    HomeProfile, Experience, Skill, Project, SocialMedia,
    Contact, SiteSettings, Achievement, Language,
)


KINOFOND_DESCRIPTIONS = {
    'en': (
        "End-to-end Django platform for the National Cinema Fund of Uzbekistan. "
        "Public catalogue with genre / year / sort filters and an HTML5 player streaming "
        "MP4 / MKV / WebM from disk via HTTP Range requests. Custom admin dashboard (not "
        "Django admin) protected by email OTP with brute-force throttling, daily / monthly "
        "visitor analytics and a Codex-themed UI. Auto-sync command imports films from "
        "C:\\kinolar with optional JSON metadata and poster pickup. Production stack: "
        "PostgreSQL + Redis + Nginx X-Accel-Redirect."
    ),
    'uz': (
        "O'zbekiston Milliy Kinofondi uchun to'liq Django platforma. Janr / yil / saralash "
        "filtrlari bilan ommaviy katalog va diskdagi MP4 / MKV / WebM fayllarni HTTP Range "
        "orqali oqib beruvchi HTML5 pleyer. Custom admin paneli (Django admin emas) — "
        "email-OTP, brute-force himoyasi, kunlik / oylik analitika va Codex dizayni. "
        "C:\\kinolar papkasidan filmlarni JSON metadata va afishalar bilan avto-sinxronlash. "
        "Production: PostgreSQL + Redis + Nginx X-Accel-Redirect."
    ),
    'ru': (
        "Полная Django-платформа для Национального Кинофонда Узбекистана. Публичный каталог "
        "с фильтрами по жанру / году / сортировке и HTML5-плеер, стримящий MP4 / MKV / WebM "
        "с диска через HTTP Range. Кастомная админ-панель (не Django admin) с защитой "
        "email-OTP, антибрут-форсом, аналитикой посещений и дизайном Codex. Авто-синхронизация "
        "фильмов из C:\\kinolar с JSON-метаданными и обложками. Production: PostgreSQL + Redis "
        "+ Nginx X-Accel-Redirect."
    ),
}

KINOFOND_TECH = (
    'Django · PostgreSQL · Redis · Nginx · HTML5 Video '
    '· HTTP Range · Email OTP · X-Accel-Redirect · Codex UI'
)


# Skill name + Technical Arsenal section. Covers the general stack plus
# everything the KinoFond zip uses.
TECHNICAL_ARSENAL = [
    # core backend
    ('Python', 'BACKEND_DEVELOPMENT'),
    ('Django', 'BACKEND_DEVELOPMENT'),
    ('Django ORM', 'BACKEND_DEVELOPMENT'),
    ('Django Admin (custom)', 'BACKEND_DEVELOPMENT'),
    ('Django REST Framework', 'BACKEND_DEVELOPMENT'),
    ('FastAPI', 'BACKEND_DEVELOPMENT'),
    ('PostgreSQL', 'BACKEND_DEVELOPMENT'),
    ('Redis', 'BACKEND_DEVELOPMENT'),
    ('Email OTP auth', 'BACKEND_DEVELOPMENT'),
    ('HMAC / timing-safe compare', 'BACKEND_DEVELOPMENT'),
    ('HTTP Range streaming', 'BACKEND_DEVELOPMENT'),
    ('Telegram Bot API', 'BACKEND_DEVELOPMENT'),
    ('aiogram', 'BACKEND_DEVELOPMENT'),
    # devops
    ('Docker', 'DEVOPS_AND_CLOUDING'),
    ('Nginx', 'DEVOPS_AND_CLOUDING'),
    ('Nginx X-Accel-Redirect', 'DEVOPS_AND_CLOUDING'),
    ('Gunicorn', 'DEVOPS_AND_CLOUDING'),
    ('Linux', 'DEVOPS_AND_CLOUDING'),
    ('Render / Railway deploy', 'DEVOPS_AND_CLOUDING'),
    # AI / ML
    ('OpenAI API', 'AI_AND_MACHINELEARNING'),
    ('AI Agents', 'AI_AND_MACHINELEARNING'),
    ('LangChain', 'AI_AND_MACHINELEARNING'),
    ('Prompt Engineering', 'AI_AND_MACHINELEARNING'),
    ('Vector DBs', 'AI_AND_MACHINELEARNING'),
    # data & frontend
    ('JavaScript', 'DATA_AND_FRONTEND'),
    ('HTML / CSS', 'DATA_AND_FRONTEND'),
    ('HTML5 Video player', 'DATA_AND_FRONTEND'),
    ('Pandas', 'DATA_AND_FRONTEND'),
]


def backfill_translations(model, base_fields):
    """For every row, mirror the legacy single-language field into empty _en/_uz/_ru
    (and the other direction if the legacy field is empty but _en is set)."""
    for row in model.objects.all():
        changed = False
        for f in base_fields:
            legacy = getattr(row, f, '') or ''
            for suffix in ('_en', '_uz', '_ru'):
                tf = f + suffix
                if not hasattr(row, tf):
                    continue
                if not getattr(row, tf):
                    setattr(row, tf, legacy)
                    changed = True
            if not legacy and hasattr(row, f + '_en') and getattr(row, f + '_en'):
                setattr(row, f, getattr(row, f + '_en'))
                changed = True
        if changed:
            row.save()


def dedupe_to_one(qs):
    """Keep only the lowest-id row, delete the rest. Returns the kept row (or None)."""
    rows = list(qs.order_by('id'))
    if not rows:
        return None, 0
    extras = rows[1:]
    for r in extras:
        r.delete()
    return rows[0], len(extras)


class Command(BaseCommand):
    help = "Reset CV to a single KinoFond entry and refresh multilingual content."

    def handle(self, *args, **options):
        kw = 'kinofond'

        # ---------- 1. Remove non-KinoFond Experience / Project ----------
        exp_killed = 0
        for e in Experience.objects.all():
            name = (e.project_name_en or e.project_name or '').lower()
            if kw not in name:
                e.delete()
                exp_killed += 1

        proj_killed = 0
        for p in Project.objects.all():
            name = (p.name_p_en or p.name_p or '').lower()
            if kw not in name:
                p.delete()
                proj_killed += 1

        # ---------- 2. Dedupe KinoFond Experience / Project to one each ----------
        kept_exp, exp_dup = dedupe_to_one(
            Experience.objects.filter(project_name_en__icontains=kw)
            | Experience.objects.filter(project_name__icontains=kw)
        )
        kept_proj, proj_dup = dedupe_to_one(
            Project.objects.filter(name_p_en__icontains=kw)
            | Project.objects.filter(name_p__icontains=kw)
        )

        self.stdout.write(self.style.WARNING(
            f"[cleanup] removed {exp_killed} non-KinoFond experiences "
            f"({exp_dup} dup), {proj_killed} non-KinoFond projects ({proj_dup} dup)"
        ))

        # ---------- 3. Home profile refreshed in 3 langs ----------
        hp = HomeProfile.objects.first() or HomeProfile()
        hp.job_en = 'AI Specialist and Backend Developer'
        hp.job_uz = 'AI mutaxassis va Backend dasturchi'
        hp.job_ru = 'AI-специалист и Backend-разработчик'
        hp.job = hp.job_en
        if not hp.about_me_en:
            hp.about_me_en = (
                "I'm a passionate backend developer focused on building scalable digital solutions "
                "that solve real-world problems. I specialize in Python technologies — particularly "
                "FastAPI, Django, REST APIs and modern backend architectures. I enjoy designing APIs "
                "and exploring intelligent bots powered by AI. I strongly believe in continuous "
                "learning, AI–backend integration, clean code and building reliable systems."
            )
        if not hp.about_me_uz:
            hp.about_me_uz = (
                "Men real dunyo muammolarini hal qiluvchi scalable raqamli yechimlar qurishga "
                "qiziquvchan backend dasturchiman. Python texnologiyalari — ayniqsa FastAPI, "
                "Django, REST API va zamonaviy backend arxitekturalariga ixtisoslashganman. "
                "API'lar dizayni va AI quvvati bilan ishlovchi aqlli botlar bilan ishlashni "
                "yaxshi ko'raman. Backend sohasini doimiy o'rganish, AI bilan tizim integratsiyasi, "
                "toza kod va mustahkam tizimlar qurishga ishonaman."
            )
        if not hp.about_me_ru:
            hp.about_me_ru = (
                "Я страстный backend-разработчик, нацеленный на создание масштабируемых "
                "цифровых решений, которые решают реальные задачи. Специализируюсь на Python — "
                "особенно FastAPI, Django, REST API и современных backend-архитектурах. "
                "Люблю проектировать API и исследовать интеллектуальных ботов на базе AI. "
                "Верю в постоянное обучение, интеграцию AI и backend, чистый код и "
                "построение надёжных систем."
            )
        if not hp.about_me:
            hp.about_me = hp.about_me_en
        hp.save()
        self.stdout.write(self.style.SUCCESS('[ok] HomeProfile refreshed'))

        # ---------- 4. KinoFond Experience (single, refreshed) ----------
        kino = kept_exp or Experience()
        kino.project_name = 'KinoFond — Uzbekistan National Cinema Fund'
        kino.project_name_en = 'KinoFond — Uzbekistan National Cinema Fund'
        kino.project_name_uz = "KinoFond — O'zbekiston Milliy Kinofondi"
        kino.project_name_ru = 'KinoFond — Национальный Кинофонд Узбекистана'
        kino.start_date = date(2026, 3, 1)
        kino.end_date = None
        kino.description = KINOFOND_DESCRIPTIONS['en']
        kino.description_en = KINOFOND_DESCRIPTIONS['en']
        kino.description_uz = KINOFOND_DESCRIPTIONS['uz']
        kino.description_ru = KINOFOND_DESCRIPTIONS['ru']
        kino.order = 0
        kino.save()
        self.stdout.write(self.style.SUCCESS('[ok] KinoFond Experience'))

        # ---------- 5. KinoFond Project (single, refreshed) ----------
        proj = kept_proj or Project()
        proj.name_p = 'KinoFond — National Cinema Fund'
        proj.name_p_en = 'KinoFond — National Cinema Fund'
        proj.name_p_uz = 'KinoFond — Milliy Kinofond'
        proj.name_p_ru = 'KinoFond — Национальный Кинофонд'
        proj.work_description_en = (
            "Django + PostgreSQL + Redis. Video streaming with HTTP Range, custom email-OTP "
            "admin, C:\\kinolar auto-sync, multilingual public catalogue, full analytics dashboard."
        )
        proj.work_description_uz = (
            "Django + PostgreSQL + Redis. HTTP Range orqali video streaming, email-OTP admin "
            "paneli, C:\\kinolar avto-sinxronlash, ko'p tilli katalog, to'liq analitika dashboardi."
        )
        proj.work_description_ru = (
            "Django + PostgreSQL + Redis. Видео-стриминг через HTTP Range, "
            "кастомная админ-панель с email-OTP, "
            "авто-синхронизация C:\\kinolar, мультиязычный каталог, аналитика."
        )
        proj.work_description = proj.work_description_en
        proj.technologies = KINOFOND_TECH
        proj.order = 0
        proj.save()
        self.stdout.write(self.style.SUCCESS('[ok] KinoFond Project'))

        # ---------- 6. Technical Arsenal (skills): KinoFond tech included ----------
        existing = {s.skill_name.lower() for s in Skill.objects.all()}
        added = 0
        for name, section in TECHNICAL_ARSENAL:
            if name.lower() in existing:
                continue
            Skill.objects.create(skill_name=name, section=section)
            existing.add(name.lower())
            added += 1
        self.stdout.write(self.style.SUCCESS(f'[ok] Technical Arsenal: +{added} skills (no dups)'))

        # ---------- 7. Contact + Social (only if empty) ----------
        if not Contact.objects.exists():
            Contact.objects.create(
                email='nazarbeksafarov895@gmail.com',
                phone='+998 91 833 65 35',
                location='Uzbekistan, Tashkent',
                location_en='Uzbekistan, Tashkent',
                location_uz="O'zbekiston, Toshkent",
                location_ru='Узбекистан, Ташкент',
            )
            self.stdout.write(self.style.SUCCESS('[ok] Contact'))

        if not SocialMedia.objects.exists():
            SocialMedia.objects.create(
                github='https://github.com/Nazarbek-1213',
                linkedin='https://www.linkedin.com/in/nazarbek-safarov-6390ab3b2/',
                telegram='https://web.telegram.org/k/#@Safarov_Nazarbek',
                instagram='https://www.instagram.com/nazarbek_safarov1/',
            )
            self.stdout.write(self.style.SUCCESS('[ok] SocialMedia'))

        # ---------- 8. Languages ----------
        lang_defaults = [
            # name_en, name_uz, name_ru, level_en, level_uz, level_ru, flag, order
            ('English',  'Ingliz',    'Английский', 'Fluent',          'Yuqori daraja',    'Свободно',         '🇬🇧', 0),
            ('Russian',  'Rus',       'Русский',    'Pre-Intermediate','Pre-Intermediate', 'Pre-Intermediate', '🇷🇺', 1),
            ('Uzbek',    "O'zbek",    'Узбекский',  'Native',          'Ona tili',         'Родной',           '🇺🇿', 2),
        ]
        lang_added = 0
        for n_en, n_uz, n_ru, l_en, l_uz, l_ru, flag, order in lang_defaults:
            obj, created = Language.objects.get_or_create(
                name_en=n_en,
                defaults=dict(
                    name=n_en, name_uz=n_uz, name_ru=n_ru,
                    level=l_en, level_en=l_en, level_uz=l_uz, level_ru=l_ru,
                    flag=flag, order=order,
                ),
            )
            if created:
                lang_added += 1
        self.stdout.write(self.style.SUCCESS(f'[ok] Languages: +{lang_added}'))

        # ---------- 9. Achievement: combined diploma PDF + PNG preview ----------
        diploma_png = 'achievements/diplomas_combined.png'
        diploma_pdf = 'achievements/diplomas_combined.pdf'
        ach = Achievement.objects.filter(photo=diploma_png).first()
        if ach is None and not Achievement.objects.exists():
            ach = Achievement.objects.create()
        if ach is not None:
            ach.name_a_en = 'Diplomas & Certificates'
            ach.name_a_uz = 'Diplomlar va sertifikatlar'
            ach.name_a_ru = 'Дипломы и сертификаты'
            ach.name_a = ach.name_a_en
            if not ach.description_en:
                ach.description_en = (
                    "Combined certificate: 8-month backend course at Najot Ta'lim with 5+ "
                    "self-built projects, plus additional certificate. Currently part-time "
                    "backend developer at a state organisation."
                )
            if not ach.description_uz:
                ach.description_uz = (
                    "Birlashtirilgan sertifikat: Najot Ta'lim'da 8 oylik backend kursi "
                    "(5+ shaxsiy loyiha) va qo'shimcha sertifikat. Hozir davlat tashkilotida "
                    "part-time backend dasturchi."
                )
            if not ach.description_ru:
                ach.description_ru = (
                    "Объединённый сертификат: 8-месячный курс backend в Najot Ta'lim "
                    "с 5+ собственными проектами плюс дополнительный сертификат. "
                    "Сейчас part-time backend-разработчик в государственной организации."
                )
            if not ach.description:
                ach.description = ach.description_en
            ach.photo = diploma_png
            ach.pdf_file = diploma_pdf
            ach.save()
            self.stdout.write(self.style.SUCCESS('[ok] Achievement: diploma'))

        # ---------- 10. Site settings ----------
        site = SiteSettings.get()
        if not site.footer_signature:
            site.footer_signature = 'Powered by Nazarbek'
        site.save()
        self.stdout.write(self.style.SUCCESS('[ok] SiteSettings'))

        # ---------- 11. Backfill 3-lang fields everywhere ----------
        backfill_translations(HomeProfile, ['about_me', 'job'])
        backfill_translations(Experience, ['project_name', 'description'])
        backfill_translations(Project, ['name_p', 'work_description'])
        backfill_translations(Achievement, ['name_a', 'description'])
        backfill_translations(Contact, ['location'])
        self.stdout.write(self.style.SUCCESS('[ok] backfilled _uz / _ru / _en on all rows'))

        self.stdout.write(self.style.SUCCESS('All done.'))
