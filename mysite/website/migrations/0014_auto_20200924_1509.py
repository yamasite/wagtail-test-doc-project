# Generated by Django 3.0.10 on 2020-09-24 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_auto_20200924_1506'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='docpagewithmediaandreusesupport',
            options={'ordering': ['-first_published_at'], 'verbose_name': 'Doc page with media and reuse support'},
        ),
        migrations.AlterModelOptions(
            name='docpagewithmediaandreusesupportandmenu',
            options={'ordering': ['-first_published_at'], 'verbose_name': '(DO NOT USE) Doc page with media and reuse , menu support'},
        ),
    ]