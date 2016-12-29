from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=50, label=False,
                               widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}))
    first_name = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    last_name = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Apellidos'}))
    email = forms.CharField(label=False, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(label=False, widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))
    password2 = forms.CharField(label=False, widget=forms.PasswordInput(attrs={'placeholder': 'Repite la contraseña'}))

    def clean(self):

        user_exists = User.objects.filter(username=self.cleaned_data.get("username"))

        if len(user_exists) != 0:
            raise ValidationError('Ese usuario ya existe')


        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError('Las contraseñas no coinciden')


        # class SignUpForm(UserCreationForm):
        #
        #     class Meta:
        #         model = User
        #         fields =['username', 'first_name', 'last_name', 'email', "password1", "password2"]

