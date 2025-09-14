from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile

class RegisterFrom(UserCreationForm):
  email = forms.EmailField(required=True)
  
  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2', 'role']
    
class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['phone', 'address']