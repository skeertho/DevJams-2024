# Generated by Django 5.1.1 on 2024-09-20 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quackpack', '0002_alter_students_mob'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='students',
            name='address',
        ),
    ]
