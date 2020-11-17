# Generated by Django 3.1.2 on 2020-11-14 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yfcases', '0014_auto_20201111_0333'),
    ]

    operations = [
        migrations.AddField(
            model_name='yfcase',
            name='yfcaseAgent',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='代理人'),
        ),
        migrations.AddField(
            model_name='yfcase',
            name='yfcaseDateOfCause',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='原因發生日期'),
        ),
        migrations.AddField(
            model_name='yfcase',
            name='yfcaseReasonForRegistration',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='登記原因'),
        ),
        migrations.AddField(
            model_name='yfcase',
            name='yfcaseRegistrationNote',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='登記備註'),
        ),
    ]