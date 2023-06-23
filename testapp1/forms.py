from django import forms
from .models import Recruiter, Consultant, Submissions
from django.contrib.auth import get_user_model


class SignupForm(forms.Form):
    recruiter_username  = forms.CharField(max_length=100, label = 'Username')
    password = forms.CharField(label = 'Password',widget=forms.PasswordInput)
    recruiter_name = forms.CharField(label='Recruiter Name', max_length=100)

    def save(self):
        R_UserName = self.cleaned_data['recruiter_username']
        password = self.cleaned_data['password']
        R_Name = self.cleaned_data['recruiter_name']

        Recruiter.objects.create_user(
            R_UserName=R_UserName,
            password=password,
            R_Name=R_Name
        )