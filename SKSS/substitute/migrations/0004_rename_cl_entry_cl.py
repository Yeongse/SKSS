# Generated by Django 4.1 on 2022-09-06 04:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('substitute', '0003_classleader_qualification_alter_classleader_courses'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='CL',
            new_name='cl',
        ),
    ]
