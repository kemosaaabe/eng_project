from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators


class AdvUser(AbstractUser):
    image = models.ImageField(blank=True, null=True, upload_to='')

    class Meta(AbstractUser.Meta):
        pass


class Module(models.Model):
    author = models.ForeignKey('AdvUser', on_delete=models.PROTECT, verbose_name='Автор',
                               blank=True, null=True)
    name = models.CharField(max_length=200, verbose_name='Модуль')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'


class Card(models.Model):
    module = models.ForeignKey('Module', on_delete=models.CASCADE)
    russian_translate = models.CharField(max_length=200, verbose_name='Русский перевод',
                                         validators=[validators.RegexValidator(
                                             regex=r'[А-ЯЁа-яё]+',
                                             message='Введите слово на русском языке'
                                         )])
    eng_translate = models.CharField(max_length=200, verbose_name='Английский перевод',
                                     validators=[validators.RegexValidator(
                                         regex=r'[A-Za-z]+',
                                         message='Введите слово на английском языке'
                                     )])
    image = models.ImageField(blank=True, null=True, upload_to='')

    def __str__(self):
        return self.russian_translate

    class Meta:
        verbose_name = 'Слово'
        verbose_name_plural = 'Слова'


# Tests

class Test(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Question(models.Model):
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Тест')
    text = models.TextField(verbose_name='Текст вопроса')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_right = models.BooleanField()

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'
