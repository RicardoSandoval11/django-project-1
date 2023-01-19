from django.shortcuts import render
from django.views.generic import TemplateView

# El siguiente mixin sirve para determinar si el usuario esta autenticado o no.
from django.contrib.auth.mixins import LoginRequiredMixin


from django.urls import reverse_lazy

import datetime

class HomePage(LoginRequiredMixin ,TemplateView):
    template_name= 'home/index.html'
    # La siguiente url es a donde se redirecciona a los usuarios no logueados
    login_url = reverse_lazy('users_app:user-login')

class FechaMixin(object):

    """
        la siguiente funcion se usa cuando se quiere enviar 
        un contexto al template.
    """
    def get_context_data(self, **kwargs):
        context = super(FechaMixin, self).get_context_data(**kwargs)
        context['fecha'] = datetime.datetime.now()
        return context


class TemplatePruebaMixin(FechaMixin,TemplateView):
    """
    Como esta vista hereda el mixin, esta vista es capaz de 
    trabajar con el contexto establecido en el mixin.
    """
    template_name= 'home/mixin.html'
    