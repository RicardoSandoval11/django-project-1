from django import forms

from .models import User

from django.contrib.auth import authenticate



class UserRegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )
    )

    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir contraseña'
            }
        )
    )


    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'nombres',
            'apellidos',
            'genero',
        )
    
    """
    La siguiente funcion sirve para validar que ambas 
    contraseñas ingresadas sean iguales.

    self.add_error sirve para agregar un error en el campo 
    del formulario que se especifique cuando la condicion no 
    se cumple.
    """
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas ingresadas son distinas')

        if len(str(self.cleaned_data['password1'])) < 6:
            print(len(str(self.cleaned_data['password1'])))
            self.add_error('password1', 'Las contraseñas debe de ser mayor a 6 caracteres')


class LoginForm(forms.Form):
    username = forms.CharField(
        label='username',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username'
            }
        )
    )
    password = forms.CharField(
        label='password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password'
            }
        )
    )
    """ 
        Cuando se quiere validar un formulario y no un campo 
        en especifico, se coloca solo clear.
    """
    def clean(self):
        """ 
            la siguiente linea se coloca para que la funcion 
            pueda retornar algo, debido a que no se esta 
            interactuando con algun campo en especifico.
        """
        cleaned_data = super(LoginForm,self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Los datos de tu usuario no son correctos')
        
        return self.cleaned_data


"""
    Mixing:

    Es una clase que puede ser utilizada como base para crear 
    otras clases. Las clases heredan los atributos del mixing 
    y posteriormente pueden ser personalizadas.

    Una clase permite heredar de mas de un mixing.
"""

class UpdatePasswordForm(forms.Form):

    password1 = forms.CharField(
        label='Contraseña actual',
        required=True,
        widget=forms.PasswordInput (
            attrs={
                'placeholder': 'Contraseña actual'
            }
        )
    )

    password2 = forms.CharField(
        label='Contraseña nueva',
        required=True,
        widget=forms.PasswordInput (
            attrs={
                'placeholder': 'Contraseña nueva'
            }
        )
    )

class VerificationForm(forms.Form):
    codregistro = forms.CharField(required=True)

    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)

    def clean_codregistro(self):
        codigo = self.cleaned_data['codregistro']

        if len(codigo) == 6:
            # verificacion si el codigo y el id del usuario son validos
            activo = User.objects.cod_validation(
                self.id_user,
                codigo
            )
            if not activo:
                raise forms.ValidationError('Invalid code') 
        else:
            raise forms.ValidationError('Invalid code')   

