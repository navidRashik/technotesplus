# Generated by Django 3.2.7 on 2021-09-07 17:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0002_alter_notes_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharedunseennotes',
            name='note',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_unseen_notes', to='notes.notes'),
        ),
        migrations.AlterField(
            model_name='sharedunseennotes',
            name='shared_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_unseen_notes', to=settings.AUTH_USER_MODEL),
        ),
    ]
