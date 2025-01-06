from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import PasswordInput, ModelForm
from django.core.validators import validate_email
from .models import *

Master = settings.AUTH_USER_MODEL

class AppointmentForm(forms.Form):
    class Meta:
        model = Appointment
        fields = {'master', 'service', 'date', 'time'}

    def clean_date(self):
        date = self.cleaned_data['date']
        return date


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='Username')
    password = forms.CharField(required=True, label='Пароль')


class MastersLoginForm(forms.Form):
    username = forms.CharField(required=True, label='Username')
    password = forms.CharField(required=True, label='Пароль')



class RegisterForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'phone']

    username = forms.CharField(min_length=3, max_length=10, required=True, label='Никнейм', validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9]*$',
            message='Может содержать только латинские буквы и цифры',
            code='invalid_username'
        ),
    ])

    email = forms.CharField(min_length=3, required=True, label='Email')
    phone = forms.CharField(min_length=11, required=True, label='Номер телефона', validators=[
        RegexValidator(
            regex='^[0-9]*$',
            message='Может содержать только цифры',
            code='invalid_number_phone'),
    ])

    password = forms.CharField(widget=PasswordInput(), required=True, label='Пароль')
    password_confirm = forms.CharField(widget=PasswordInput(), required=True, label='Повторите пароль')

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError(
                {'password_confirm': "Пароли не совпадают", 'password': ''}
            )
        username = self.cleaned_data.get("username")

        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError({'username': "Такой логин уже занят"})

        try:
            validate_email(self.cleaned_data.get("email"))
        except ValidationError:
            raise forms.ValidationError({'email': "Email не является валидным адресом"})

        return cleaned_data


class MastersRegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'fio', 'experience', 'phone', 'password', 'password_confirm')

    username = forms.CharField(min_length=3, max_length=50, required=True, label='Username', validators=[
        RegexValidator(regex='^[a-zA-Z0-9]*$', message='Может содержать только латинские буквы и цифры', code='invalid_username'),])

    fio = forms.CharField(min_length=3, max_length=100, required=True, label='Фамилия Имя Отчество', validators=[
        RegexValidator(regex='^[а-яА-Я\s]*$', message='Может содержать только буквы русского языка', code='invalid_fio'),])

    experience = forms.IntegerField()

    phone = forms.CharField(max_length=11, required=True, label='Номер телефона', validators=[
        RegexValidator(regex='^[0-9]*$', message='Может содержать только цифры', code='invalid_number_phone'),])

    password = forms.CharField(widget=PasswordInput(), required=True, label='Пароль')
    password_confirm = forms.CharField(widget=PasswordInput(), required=True, label='Повторите пароль')

    def save(self, commit=True):
        user=super().save(commit=False)
        user.is_master =True
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super(MastersRegisterForm, self).clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError(
                {'password_confirm': "Пароли не совпадают", 'password': ''}
            )
        username = self.cleaned_data.get("username")

        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError({'username': "Такой логин уже занят"})

        return cleaned_data

