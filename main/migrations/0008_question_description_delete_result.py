# Generated by Django 4.0.4 on 2022-04-22 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_test_result_question_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='description',
            field=models.TextField(null=True, verbose_name='Описание'),
        ),
        migrations.DeleteModel(
            name='Result',
        ),
    ]
