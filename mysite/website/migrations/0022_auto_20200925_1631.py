# Generated by Django 3.0.10 on 2020-09-25 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0021_docpagewithmediaandreusesupportandmultilanguage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='docpagewithmediaandreusesupportandmultilanguage',
            old_name='french_link',
            new_name='chinese_link',
        ),
        migrations.RenameField(
            model_name='docpagewithmediaandreusesupportandmultilanguage',
            old_name='spanish_link',
            new_name='japanese_link',
        ),
    ]
