# Generated by Django 4.1.1 on 2022-10-08 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('APIVIEW', '0006_developers'),
    ]

    operations = [
        migrations.AddField(
            model_name='developer',
            name='lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='developer_leads', to='APIVIEW.lead'),
        ),
        migrations.AddField(
            model_name='developer',
            name='project_manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='developer_project_managers', to='APIVIEW.projectmanager'),
        ),
    ]