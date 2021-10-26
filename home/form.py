from django.contrib.auth.models import Group, User
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.db import models


# Below.. we create a class and extend pre-defined class UserCreateionForm
class SignUpForm(UserCreationForm):
    password2 = forms.CharField(
        label='Confirm Password (Again)', widget=forms.PasswordInput)
    # no_of_member = forms.CharField(max_length=100)

    class Meta:
        model = User
        # here we defined labels that we want to display and password is extend by UserCreationForm
        fields = ['username', 'first_name',
                  'last_name', 'email']
        labels = {'username': 'Phone Number', 'email': 'Email'}


# class SignUpForm(UserCreationForm):
#     birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

#     class Meta:
#         model = User
#         fields = ('username', 'birth_date', 'password1', 'password2', )


# Below.. we create a class for user Profile and extend pre-defined class UserChangeForm
class UserProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        # what we show on User Profile Page
        fields = ['username', 'first_name', 'last_name',
                  'email']
        # what we show on user instead of predefined labels
        labels = {'email': 'Email Address', 'username': 'Phone'}

# Below.. we create a class for Admin Profile and extend pre-defined class UserChangeForm


class AdminProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        # what we show on User Profile Page
        fields = ['username', 'first_name',
                  'last_name', 'email']
        # what we show on user instead of predefined labels
        labels = {'email': 'Email Address', 'username': 'Phone'}
