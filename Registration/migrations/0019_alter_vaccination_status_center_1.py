# Generated by Django 3.2.9 on 2021-11-13 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Registration', '0018_alter_vaccination_status_vaccine_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccination_status',
            name='center_1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Registration.centers'),
        ),
    ]