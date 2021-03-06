# Generated by Django 2.0 on 2019-04-06 12:47

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('category', models.CharField(choices=[('MA', 'Mathematics'), ('PR', 'Programming'), ('IN', 'Informatics'), ('PH', 'Physics')], max_length=2)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=5000, null=True)),
                ('photo', models.FileField(upload_to='articles')),
                ('status', models.BooleanField(default=True)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('slug', models.SlugField(blank=True, default='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.FileField(upload_to='avatar/')),
                ('about', ckeditor_uploader.fields.RichTextUploadingField(default='About', max_length=1000)),
                ('slogan', models.CharField(default='Your slogan', max_length=500)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webcore.Article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
