# Generated by Django 5.0.1 on 2024-02-12 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_alter_report_created_alter_report_updated'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ['-created']},
        ),
    ]