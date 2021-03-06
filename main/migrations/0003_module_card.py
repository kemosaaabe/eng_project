# Generated by Django 4.0.4 on 2022-04-14 12:04

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_advuser_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Модуль')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Модуль',
                'verbose_name_plural': 'Модули',
            },
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('russian_translate', models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(message='Введите слово на русском языке', regex='[А-ЯЁа-яё]+')], verbose_name='Русский перевод')),
                ('eng_translate', models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(message='Введите слово на английском языке', regex='[A-Za-z]+')], verbose_name='Английский перевод')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.module')),
            ],
            options={
                'verbose_name': 'Слово',
                'verbose_name_plural': 'Слова',
            },
        ),
    ]
