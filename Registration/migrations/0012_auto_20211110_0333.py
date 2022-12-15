# Generated by Django 3.2.9 on 2021-11-09 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Registration', '0011_auto_20211110_0327'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vaccination_status',
            old_name='registrant',
            new_name='registrant_id',
        ),
        migrations.AddField(
            model_name='registrants',
            name='email',
            field=models.EmailField(default=None, max_length=50, unique=True, verbose_name='Email ID'),
        ),
        migrations.AddField(
            model_name='registrants',
            name='password',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='registrants',
            name='username',
            field=models.CharField(default=None, max_length=50, verbose_name='Username'),
        ),
    ]
