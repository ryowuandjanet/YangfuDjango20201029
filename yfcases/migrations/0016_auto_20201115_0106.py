# Generated by Django 3.1.2 on 2020-11-15 01:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yfcases', '0015_auto_20201114_1522'),
    ]

    operations = [
        migrations.RenameField(
            model_name='yfcase',
            old_name='yfcaseAgent',
            new_name='yfcaseDeedtaxAgent',
        ),
        migrations.RenameField(
            model_name='yfcase',
            old_name='yfcaseDateOfCause',
            new_name='yfcaseDeedtaxDateOfCause',
        ),
        migrations.RenameField(
            model_name='yfcase',
            old_name='yfcaseReasonForRegistration',
            new_name='yfcaseDeedtaxReasonForRegistration',
        ),
        migrations.RenameField(
            model_name='yfcase',
            old_name='yfcaseRegistrationNote',
            new_name='yfcaseDeedtaxRegistrationNote',
        ),
    ]