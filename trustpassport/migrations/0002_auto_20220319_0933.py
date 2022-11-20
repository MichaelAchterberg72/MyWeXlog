# Generated by Django 2.2 on 2022-03-19 09:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('enterprises', '0001_initial'),
        ('trustpassport', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='talentpassport',
            name='score_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='talent_scorer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='talentpassport',
            name='talent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='enterprisepassport',
            name='enterprise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='enterprises.Branch'),
        ),
        migrations.AddField(
            model_name='enterprisepassport',
            name='score_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='enterprise_scorer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='talentpassport',
            unique_together={('score_by', 'talent', 'date_score')},
        ),
        migrations.AlterUniqueTogether(
            name='enterprisepassport',
            unique_together={('score_by', 'enterprise', 'date_score')},
        ),
    ]