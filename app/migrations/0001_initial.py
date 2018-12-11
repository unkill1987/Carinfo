# Generated by Django 2.1.3 on 2018-12-11 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Government',
            fields=[
                ('government', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('user_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('passwd', models.CharField(max_length=20)),
                ('charge', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('insurance', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('licenceNum', models.CharField(max_length=100)),
                ('user_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('passwd', models.CharField(max_length=20)),
                ('charge', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Manufacture',
            fields=[
                ('company', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('licenceNum', models.CharField(max_length=100)),
                ('user_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('passwd', models.CharField(max_length=20)),
                ('charge', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('user_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('passwd', models.CharField(max_length=20)),
                ('passconfirm', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Repairshop',
            fields=[
                ('repairshop', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('licenceNum', models.CharField(max_length=100)),
                ('user_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('passwd', models.CharField(max_length=20)),
                ('charge', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Sellcar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serialnumber', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=100)),
                ('modelname', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('volume', models.CharField(max_length=100)),
                ('fuel', models.CharField(max_length=100)),
                ('owner', models.CharField(max_length=100)),
                ('whentobuy', models.CharField(max_length=100)),
                ('sellprice', models.CharField(max_length=100)),
                ('details', models.CharField(max_length=500)),
            ],
        ),
    ]
