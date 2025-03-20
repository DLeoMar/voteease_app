from dataclasses import fields
# import imp
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.forms.widgets import PasswordInput
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordChangeForm
from .models import *
from django.core.mail import send_mail

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus':False})
    """
    A Custom form for creating new users.
    """
    USER_TYPE = [('Admin', 'Admin'),
                ('Student', 'Student')]
                 

    
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Username', 'id' : 'username'}))
    user_type = forms.CharField(required=True, label="User Type:", widget=forms.Select(choices=USER_TYPE, attrs={'class' : 'custom-select', 'id' : 'userTypeSelect'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'First Name', 'id' : 'firstname'}))
    middle_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Middle Name', 'id' : 'middlename'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Last Name', 'id' : 'lastname'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'name' : 'email', 'type' : 'email', 'id' : 'email', 'placeholder': 'Enter your email address'}))
    password1 = forms.CharField(required=True,widget=PasswordInput(attrs={'type' : 'password', 'id' : 'password', 'aria-describeby' : 'passwordHelpBlock', 'placeholder':'Enter your Password', 'data-toggle': 'password'}))
    password2 = forms.CharField(required=True,widget=PasswordInput(attrs={'type' : 'password', 'id' : 'cpassword', 'placeholder':'Confirm Your Password','data-toggle': 'password'}))
    class Meta:
        model = get_user_model()
        fields = ['user_type', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def save(self):
        user = super().save(commit=False)
        user.username = self.cleaned_data.get('username')
        user.user_type = self.cleaned_data.get('user_type')
        user.first_name = self.cleaned_data.get('first_name')
        user.middle_name = self.cleaned_data.get('middle_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.password1 = self.cleaned_data.get('password1')
        user.password2 = self.cleaned_data.get('password2')
        user.save()

        return user
    

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['position_name', 'vote_count']
    
    vote_count = forms.IntegerField(required=False, initial=1)

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Ensure vote_count is set to 1 if not provided
        if not instance.vote_count:
            instance.vote_count = 1
        
        if commit:
            instance.save()
        return instance

class CandidateForm(forms.ModelForm):
    position = forms.ModelChoiceField(queryset=Position.objects.all(), required=True, empty_label="Select a Position")

    class Meta:
        model = Candidate
        fields = ['first_name', 'last_name', 'sex', 'strand', 'ps_image', 'position']

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution_name', 'start_year', 'end_year', 'description']

class LeadershipExperienceForm(forms.ModelForm):
    class Meta:
        model = LeadershipExperience
        fields = ['position', 'organization', 'start_year', 'end_year', 'description']

class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        fields = ['award_name', 'year', 'description']