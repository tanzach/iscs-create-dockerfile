# Generated by Django 4.1.6 on 2023-04-30 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myinventoryapp', '0003_alter_waterbottle_cost_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
    ]