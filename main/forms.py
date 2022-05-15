from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.core import validators
from .models import AdvUser
from .models import Module, Card
from .models import Test, Answer, Question


class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)',
                                widget=forms.PasswordInput,
                                help_text='Введите тот же самый пароль еще раз для проверки')

    image = forms.ImageField(label='Изображение',
                             widget=forms.FileInput(attrs={'class': 'custom-image'}),
                             required=False)

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise ValidationError('Пароли не совпадают')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.save()
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'password1', 'password2', 'first_name',
                  'last_name', 'image')


class UserChangeForm(forms.ModelForm):
    image = forms.ImageField(label='Изображение',
                             widget=forms.FileInput(attrs={'class': 'custom-image'}),
                             required=False)

    class Meta:
        model = AdvUser
        fields = ('username', 'first_name', 'last_name', 'image')


class ModuleForm(forms.ModelForm):
    name = forms.CharField(label='Название')

    class Meta:
        model = Module
        fields = '__all__'
        widgets = {'author': forms.HiddenInput}


class CardForm(forms.ModelForm):
    image = forms.ImageField(required=False, label='Изображение',
                             validators=[validators.FileExtensionValidator(
                                 allowed_extensions={'gif', 'jpg', 'jpeg', 'png'},
                             )],
                             error_messages={
                                 'invalid_extension': 'Этот формат не поддерживается'
                             })

    class Meta:
        model = Card
        fields = '__all__'
        widgets = {'module': forms.HiddenInput}


CardFormSet = inlineformset_factory(Module, Card, form=CardForm, fields='__all__', extra=5)
