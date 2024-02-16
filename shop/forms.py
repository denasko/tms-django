from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment


class RegistrationForm(UserCreationForm):
    """
    Форма для регистрации новых пользователей.

    Attributes:
        first_name (CharField): Поле для ввода имени пользователя (необязательное).
        last_name (CharField): Поле для ввода фамилии пользователя (необязательное).
        email (EmailField): Поле для ввода адреса электронной почты пользователя.

    Meta:
        model (User): Модель, связанная с формой.
        fields (list): Список полей, которые будут отображены в форме регистрации.

    """
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class FeedbackForm(forms.Form):
    feedback_text = forms.CharField(label='Inter your feedback', widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
