# Generated by Django 4.1.6 on 2023-05-07 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myinventoryapp', '0006_employee_payslip_delete_account_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payslip',
            name='date_range',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='payslip',
            name='month',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='payslip',
            name='year',
            field=models.CharField(max_length=4),
        ),
    ]