from django import forms
from django.contrib.auth.models import User
import re

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    def clean_username(self):
        u = self.cleaned_data['username']
        if User.objects.filter(username=u).exists():
            raise forms.ValidationError('El usuario ya existe.')
        return u

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password','')
        p2 = cleaned.get('password2','')

        if len(p1) < 8:
            self.add_error('password', 'La contraseña debe tener al menos 8 caracteres.')
        if not re.search(r'[A-Z]', p1):
            self.add_error('password', 'Debe incluir al menos una mayúscula.')
        if not re.search(r'\d', p1):
            self.add_error('password', 'Debe incluir al menos un número.')
        if not re.search(r'[^A-Za-z0-9]', p1):
            self.add_error('password', 'Debe incluir al menos un carácter especial.')

        if p1 != p2:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        return cleaned
