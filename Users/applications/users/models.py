from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager

# Create your models here.

"""
    Abstract user es una clase que permite gestionar 
    usuarios en una aplicacion.
"""

class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otros'),
    )

    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField()
    nombres = models.CharField(max_length=30, blank=True)
    apellidos = models.CharField(max_length=30, blank=True)
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    is_staff = models.BooleanField(default=False)

    # codigo de verificacion de registro
    codregistro = models.CharField(max_length=6, blank=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    """
    La siguiente variable sirve para especificar que 
    campos son obligatorios en la creacion de un registro 

    """
    REQUIRED_FIELDS = ['email',]

    objects = UserManager()

    def get_shor_name(self):
        return self.username

    def get_full_name(self):
        return self.nombres + ' ' + self.apellidos
