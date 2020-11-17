# Generated by Django 3.1.2 on 2020-11-16 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yfcases', '0020_auto_20201116_0312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yfcase',
            name='yfcaseDeedtaxDeclarationDate',
            field=models.DateField(blank=True, null=True, verbose_name='契稅申報日期'),
        ),
        migrations.AlterField(
            model_name='yfcase',
            name='yfcaseDeedtaxEstablishmentDate',
            field=models.DateField(blank=True, null=True, verbose_name='契稅建立日期'),
        ),
        migrations.AlterField(
            model_name='yfcase',
            name='yfcaseDeedtaxHouseTaxRegistrationNumber',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='房屋稅籍編號'),
        ),
    ]