from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from . import models


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Придумайте логин', widget=forms.TextInput(attrs={'class': 'form_input'}))
    email = forms.EmailField(label='Введите Email', widget=forms.EmailInput(attrs={'class': 'form_input'}))
    password1 = forms.CharField(label='Придумайте пароль', widget=forms.PasswordInput(attrs={'class': 'form_input'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form_input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form_input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form_input'}))


class CommentsForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'comment_form',
            'placeholder': 'Напишите комментарий',
        }),
        label=''
    )

    class Meta:
        model = models.CommentMovie
        fields = ['content']
