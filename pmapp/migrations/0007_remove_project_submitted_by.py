# Generated by Django 3.2.9 on 2022-01-31 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pmapp', '0006_auto_20220201_0026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='submitted_by',
        ),
    ]