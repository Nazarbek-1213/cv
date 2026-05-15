from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0003_translations_and_settings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitesettings',
            name='background_music',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='music_volume',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='admin_trigger_word',
        ),
    ]
