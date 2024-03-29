# Generated by Django 3.0.7 on 2020-09-11 07:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=30)),
                ('status', models.BooleanField(default=True)),
                ('img_1', models.ImageField(upload_to='static/upload_tumb/')),
                ('img_2', models.ImageField(upload_to='static/upload_tumb/')),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.Categories')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vote_img1', models.ManyToManyField(blank=True, related_name='img_1', to=settings.AUTH_USER_MODEL)),
                ('vote_img2', models.ManyToManyField(blank=True, related_name='img_2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
