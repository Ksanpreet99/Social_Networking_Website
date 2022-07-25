from dataclasses import fields
from operator import mod
from pyexpat import model
from statistics import mode
from typing_extensions import Required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from .models import *



class CreateUserForm(UserCreationForm):
    def validate_email(value):
        if User.objects.filter(email = value).exists():
            raise ValidationError(
                (f"{value} is taken."),
                params = {'value':value}
        )
    email = forms.EmailField(validators = [validate_email])
    class Meta:
        model=User
        fields=['username','password1','password2','email']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class profile_form(forms.ModelForm):
    class Meta:
        model=User
        fields = ['username', 'email']
    
    def __init__(self, *args, **kwargs):
        super(profile_form, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None    

class edit_profile_form(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['first_name','last_name','phone_no','DOB','gender','city','country','about_me','graduate','post_graduate','g_course','p_course','study_at','p_study_at','work_as','work_at','work_city','work_country','profile_photo','cover_photo']
        widgets = {
        'DOB': forms.SelectDateWidget(years=range(2021,1990,-1)),
        'gender':forms.RadioSelect(),
    }
    def __init__(self, *args, **kwargs):
        super(edit_profile_form, self).__init__(*args, **kwargs)
        
        for fieldname in ['gender','profile_photo','cover_photo']:
            self.fields[fieldname].label = False

class user_interest_form(forms.ModelForm):
   
    class Meta:
        model=user_interest
        fields='__all__'
        
    
    def __init__(self, *args, **kwargs):
        super(user_interest_form, self).__init__(*args, **kwargs)
        self.fields['interest'].label = False
        self.fields['user'].label = False


class create_post_form(forms.ModelForm):
    class Meta:
        model=Post
        fields=['user','post_text','post_img','post_video']

    def __init__(self, *args, **kwargs):
        super(create_post_form, self).__init__(*args, **kwargs)
        for fieldname in ['post_text','post_img','post_video']:
            self.fields[fieldname].label = False
        self.fields['post_text'].widget.attrs['placeholder'] = 'write something...'
        

class comment_form(forms.ModelForm):
    class Meta:
        model=Comments
        fields=['user','post','comment_text']
    def __init__(self, *args, **kwargs):
        super(comment_form, self).__init__(*args, **kwargs)
        for fieldname in ['user','post','comment_text']:
            self.fields[fieldname].label = False

        self.fields['comment_text'].widget.attrs['placeholder'] = 'Post your comment'

        
