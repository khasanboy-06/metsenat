# Generated by Django 5.1.4 on 2024-12-17 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_alter_sponsor_sponsor_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='sponsor_type',
            field=models.CharField(choices=[('physical_person', 'Jismoniy shaxs'), ('legal_entity', 'Yuridik shaxs')], max_length=255),
        ),
    ]
