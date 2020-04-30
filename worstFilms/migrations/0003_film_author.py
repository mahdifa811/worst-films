# Generated by Django 3.0.4 on 2020-03-25 08:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('worstFilms', '0002_remove_film_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='author',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]