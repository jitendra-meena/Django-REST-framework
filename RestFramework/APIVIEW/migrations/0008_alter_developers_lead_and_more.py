# Generated by Django 4.1.1 on 2022-10-13 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('APIVIEW', '0007_developer_lead_developer_project_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developers',
            name='lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='APIVIEW.lead'),
        ),
        migrations.AlterField(
            model_name='developers',
            name='project_manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='APIVIEW.projectmanager'),
        ),
    ]
