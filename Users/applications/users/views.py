from django.shortcuts import render
from .forms import UserRegisterForm, LoginForm, UpdatePasswordForm, VerificationForm
from .models import User
from django.urls import reverse_lazy, reverse

# usada para enviar correos 
from django.core.mail import send_mail

# La siguiente importacion sirve para redireccionar al usuario
from django.http import HttpResponseRedirect

# Importacion usada para realizar login en el sistema
from django.contrib.auth import authenticate, login, logout

# Usado para que estar autenticado sea un requerimiento dentro del sistema
from django.contrib.auth.mixins import LoginRequiredMixin


from django.views.generic import (
    CreateView,
    View
)

from django.views.generic.edit import FormView

#funciones personalizadas
from .functions import code_generator

class UserRegisterView(FormView):
    template_name='users/register.html'
    form_class = UserRegisterForm

    """ para que se realice un proceso de guardado y 
        actualizado se necesita la siguiente funcion."""
    def form_valid(self, form):

        # generar el codigo
        codigo = code_generator()

        """
            El siguiente bloque de codigo sirve para crear un 
            usuario comun.
        """
        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            genero=form.cleaned_data['genero'],
            codregistro=codigo,
        )
        # enviar el codigo al correo del usuario
        asunto = 'Confirmacion de email'
        mensaje= 'Codigo de verificacion ' + codigo
        email_remitente = 'ricardosandoval344@gmal.com'

        # enviar correo
        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email']])

        # redirigir a pantalla de validacion


        # Se envia el id del usuario que se acaba de registrar por la url
        return HttpResponseRedirect(
            reverse(
                'users_app:user-verification',
                kwargs={'pk': usuario.id}
            )
        )

class LoginUser(FormView):
    template_name= 'users/login.html'
    form_class= LoginForm
    success_url= reverse_lazy('home_app:homa-page')

    def form_valid(self, form):

        """
            La siguiente validacion sirve para verificar que 
            el usuario existe en el sistema.
        """
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )

        """
            La siguiente funcionde django realiza el proceso 
            de hacer login en el sistema.
        """
        login(self.request, user)

        return super(LoginUser, self).form_valid(form)

"""
Para procesos que no requiren mostrar informacion, se utiliza 
la vista View.
"""

class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )

class UpdatePassword(LoginRequiredMixin,FormView):
    template_name = 'users/update.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')
    """ 
        Con el mixin se vuelve requerido autenticarse para 
        acceder a esta vista. Si no esta autenticado, al 
        usuario se le redirecciona a la siguiente url
    """
    login_url = reverse_lazy('users_app:user-login')

    def form_valid(self, form):

        # Se obtiene la informacion del usuario
        usuario = self.request.user

        user = authenticate(
            username=usuario.username,
            password=form.cleaned_data['password1']
        )

        # Si el usuario se autentico correctamente
        if user:
            # se obtiene el password nuevo del formulario
            new_password = form.cleaned_data['password2']
            # se encripta el password
            usuario.set_password(new_password)
            # se guardan los datos
            usuario.save()
        logout(self.request)

        return super(UpdatePassword, self).form_valid(form)

class CodeVerificationView(FormView):
    template_name= 'users/verification.html'
    form_class= VerificationForm
    success_url= reverse_lazy('users_app:user-login')

    """ 
        la siguiente funcion es usada para pasar un contexto 
        a los forms y que estos puedan obtener informacion de 
        urls
    """

    def get_form_kwargs(self):
        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk']
        })
        return kwargs

    def form_valid(self, form):

        # se actualiza el estado del usuario en la app de inactivo a activo
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active=True
        )

        return super(CodeVerificationView, self).form_valid(form)



