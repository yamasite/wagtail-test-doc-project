# Generated by Django 3.0.10 on 2020-09-24 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_docpagewithmediaandreusesupport'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleindexpage',
            name='repeat_in_subnav',
            field=models.BooleanField(default=False, help_text="If checked, a link to this page will be repeated alongside it's direct children when displaying a sub-navigation for this page.", verbose_name='repeat in sub-navigation'),
        ),
        migrations.AddField(
            model_name='articleindexpage',
            name='repeated_item_text',
            field=models.CharField(blank=True, help_text="e.g. 'Section home' or 'Overview'. If left blank, the page title will be used.", max_length=255, verbose_name='repeated item link text'),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='repeat_in_subnav',
            field=models.BooleanField(default=False, help_text="If checked, a link to this page will be repeated alongside it's direct children when displaying a sub-navigation for this page.", verbose_name='repeat in sub-navigation'),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='repeated_item_text',
            field=models.CharField(blank=True, help_text="e.g. 'Section home' or 'Overview'. If left blank, the page title will be used.", max_length=255, verbose_name='repeated item link text'),
        ),
        migrations.AddField(
            model_name='docpage',
            name='repeat_in_subnav',
            field=models.BooleanField(default=False, help_text="If checked, a link to this page will be repeated alongside it's direct children when displaying a sub-navigation for this page.", verbose_name='repeat in sub-navigation'),
        ),
        migrations.AddField(
            model_name='docpage',
            name='repeated_item_text',
            field=models.CharField(blank=True, help_text="e.g. 'Section home' or 'Overview'. If left blank, the page title will be used.", max_length=255, verbose_name='repeated item link text'),
        ),
        migrations.AddField(
            model_name='docpagewithmediaandreusesupport',
            name='repeat_in_subnav',
            field=models.BooleanField(default=False, help_text="If checked, a link to this page will be repeated alongside it's direct children when displaying a sub-navigation for this page.", verbose_name='repeat in sub-navigation'),
        ),
        migrations.AddField(
            model_name='docpagewithmediaandreusesupport',
            name='repeated_item_text',
            field=models.CharField(blank=True, help_text="e.g. 'Section home' or 'Overview'. If left blank, the page title will be used.", max_length=255, verbose_name='repeated item link text'),
        ),
        migrations.AddField(
            model_name='formpage',
            name='repeat_in_subnav',
            field=models.BooleanField(default=False, help_text="If checked, a link to this page will be repeated alongside it's direct children when displaying a sub-navigation for this page.", verbose_name='repeat in sub-navigation'),
        ),
        migrations.AddField(
            model_name='formpage',
            name='repeated_item_text',
            field=models.CharField(blank=True, help_text="e.g. 'Section home' or 'Overview'. If left blank, the page title will be used.", max_length=255, verbose_name='repeated item link text'),
        ),
        migrations.AddField(
            model_name='webpage',
            name='repeat_in_subnav',
            field=models.BooleanField(default=False, help_text="If checked, a link to this page will be repeated alongside it's direct children when displaying a sub-navigation for this page.", verbose_name='repeat in sub-navigation'),
        ),
        migrations.AddField(
            model_name='webpage',
            name='repeated_item_text',
            field=models.CharField(blank=True, help_text="e.g. 'Section home' or 'Overview'. If left blank, the page title will be used.", max_length=255, verbose_name='repeated item link text'),
        ),
    ]
