# Generated by Django 3.2.7 on 2023-06-04 10:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0003_auto_20210907_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sharedunseennotes',
            name='notified_owner',
        ),
        migrations.AddField(
            model_name='notes',
            name='note_privacy_type',
            field=models.CharField(choices=[('PUBLIC', 'Public'), ('PRIVATE', 'Private')], default='PRIVATE', max_length=20),
        ),
        migrations.AlterField(
            model_name='notes',
            name='shared_with',
            field=models.ManyToManyField(blank=True, related_name='accessible_notes', to=settings.AUTH_USER_MODEL),
        ),
    ]