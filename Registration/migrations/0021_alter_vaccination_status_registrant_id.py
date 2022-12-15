# Generated by Django 3.2.9 on 2021-11-13 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Registration', '0020_auto_20211114_0034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccination_status',
            name='registrant_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='registrants', serialize=False, to='Registration.registrants', verbose_name='Registrant ID'),
        ),
    ]
