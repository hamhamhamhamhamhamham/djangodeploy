# FORM + database >> MODEL
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms








# FORM
class NewUserForm(UserCreationForm):
    email=forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class':"focus:outline-none",'placeholder':'demo@gmail.com'}))
    username=forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'focus:outline-none','placeholder':'jasatea'}))
    password1=forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'focus:outline-none','placeholder':"+8 chars! & +use nums  "}))
    password2=forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'focus:outline-none'}))
    # MODEL
    class Meta:
        model=User  
        fields=("username","email","password1","password2")
    #Database User Registration
    def save(self,commit=True):
        user=super(NewUserForm,self).save(commit=False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user    