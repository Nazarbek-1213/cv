from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0004_drop_music_and_trigger'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievement',
            name='pdf_file',
            field=models.FileField(
                blank=True, null=True, upload_to='achievements/',
                help_text='Optional PDF (combined certificate, transcript, etc.)',
            ),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=40)),
                ('name_en', models.CharField(blank=True, default='', max_length=40)),
                ('name_uz', models.CharField(blank=True, default='', max_length=40)),
                ('name_ru', models.CharField(blank=True, default='', max_length=40)),
                ('level', models.CharField(blank=True, default='Fluent', max_length=24)),
                ('level_en', models.CharField(blank=True, default='', max_length=24)),
                ('level_uz', models.CharField(blank=True, default='', max_length=24)),
                ('level_ru', models.CharField(blank=True, default='', max_length=24)),
                ('flag', models.CharField(blank=True, default='', help_text='Optional emoji flag, e.g. 🇬🇧', max_length=8)),
                ('order', models.IntegerField(default=0)),
            ],
            options={'ordering': ['order', 'id']},
        ),
    ]
