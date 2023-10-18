from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

from . import models
from . import forms


class BaseProfile(View):
    template_name = 'profile_user/create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.profile = None

        if self.request.user.is_authenticated:
            self.profile = models.ProfileUser.objects.filter(
                user=self.request.user
            ).first()

            self.contexto = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance=self.request.user,
                ),

                'profileform': forms.ProfileForm(
                    data=self.request.POST or None
                )
            }
        else:
            self.contexto = {
                'userform': forms.UserForm(
                    data=self.request.POST or None
                ),
                'profileform': forms.ProfileForm(
                    data=self.request.POST or None
                )
            }
        self.userform = self.contexto['userform']
        self.profileform = self.contexto['profileform']
        self.render = render(self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.render


class Create(BaseProfile):
    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.profileform.is_valid():
            messages.error(
                self.request,
                'Existem erros no formulário de cadastro. Verifique se todos '
                'os campos foram preenchidos corretamente.'
            )

            return self.render

        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')

        # username = self.userform.cleaned_data.get('username')

        if self.request.user.is_authenticated:
            pass
        else:
            user = self.userform.save(commit=False)
            user.set_password(password)
            user.save()

            profile = self.profileform.save(commit=False)
            profile.set_password(password)
            profile.save()

        return self.render


class Update(View):
    pass


class Login(View):
    pass


class Logout(View):
    pass

# Create your views here.
