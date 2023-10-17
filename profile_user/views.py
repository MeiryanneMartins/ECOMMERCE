from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse

from . import models
from . import forms


class BaseProfile(View):
    template_name = 'profile_user/create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.contexto = {
            'userform': forms.UserForm(
                data=self.request.POST or None
            )
        }

        self.render = render(self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.render


class Create(BaseProfile):
    def post(self, *args, **kwargs):
        return self.render


class Update(View):
    pass


class Login(View):
    pass


class Logout(View):
    pass

# Create your views here.
