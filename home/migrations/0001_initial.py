# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-27 10:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-date_added',),
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Display',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50)),
                ('body', models.TextField()),
                ('photo', imagekit.models.fields.ProcessedImageField(blank=True, upload_to='latest')),
            ],
        ),
        migrations.CreateModel(
            name='Latest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('story', models.TextField()),
                ('created', models.DateField(auto_now_add=True)),
                ('summary', models.TextField()),
                ('slug', models.SlugField(default='latest', unique_for_date='created')),
                ('photo', imagekit.models.fields.ProcessedImageField(blank=True, upload_to='latest')),
                ('thumbnail', imagekit.models.fields.ProcessedImageField(blank=True, upload_to='latest')),
                ('status', models.CharField(choices=[('published', 'PUBLISHED'), ('draft', 'DRAFT')], default='draft', max_length=50)),
                ('priority', models.CharField(choices=[('yes', 'YES'), ('no', 'NO')], default='no', max_length=50)),
                ('video', models.URLField(blank=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Category')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50)),
                ('body', models.TextField()),
                ('photo', imagekit.models.fields.ProcessedImageField(blank=True, upload_to='latest')),
                ('person', models.CharField(blank=True, max_length=50, verbose_name='Testimonial From')),
                ('course', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Writer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('date_added', models.DateField(auto_now_add=True)),
                ('picture', imagekit.models.fields.ProcessedImageField(blank=True, upload_to='writers')),
            ],
        ),
        migrations.AddField(
            model_name='latest',
            name='writer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Writer'),
        ),
    ]
