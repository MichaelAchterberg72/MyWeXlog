# Generated by Django 2.2 on 2022-03-19 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('AppControl', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrgStructure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level_name', models.CharField(max_length=100)),
                ('corporate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppControl.CorporateHR')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parentdept', to='mod_corporate.OrgStructure')),
            ],
        ),
        migrations.CreateModel(
            name='RequiredSkills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mod_corporate.OrgStructure')),
            ],
        ),
        migrations.CreateModel(
            name='CorporateStaff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corp_access', models.SmallIntegerField(choices=[(3, 'Administrator'), (2, 'Controller'), (1, 'Department Head'), (0, 'Staff')], default=0)),
                ('status', models.BooleanField(default=False, verbose_name='Admin / Staff')),
                ('hide', models.BooleanField(default=False, verbose_name='Ignore')),
                ('date_add', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('unlocked', models.BooleanField(default=False)),
                ('resigned', models.BooleanField(default=False)),
                ('slug', models.CharField(blank=True, max_length=9)),
                ('date_from', models.DateField()),
                ('date_to', models.DateField(blank=True, null=True)),
                ('corporate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppControl.CorporateHR')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mod_corporate.OrgStructure')),
            ],
            options={
                'verbose_name_plural': 'Corporate Staff',
            },
        ),
    ]