# Generated by Django 5.0.4 on 2024-05-10 01:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ScentPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=400)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scent_posts', to='sniffapi.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scent_posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ScentReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField()),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('scent_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scent_reviews', to='sniffapi.scentpost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scent_reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ScentUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scent_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='sniffapi.scentpost')),
                ('scent_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='sniffapi.scentuser')),
            ],
        ),
        migrations.CreateModel(
            name='ScentTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scent_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scent_tag', to='sniffapi.scentpost')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scent_tag', to='sniffapi.tag')),
            ],
        ),
        migrations.AddField(
            model_name='scentpost',
            name='tags',
            field=models.ManyToManyField(related_name='scent_posts', through='sniffapi.ScentTag', to='sniffapi.tag'),
        ),
    ]
