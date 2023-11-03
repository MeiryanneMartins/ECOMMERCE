from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages


class Pay(View):
    template_name = 'order/pay.html'

    def get(self, *args, **kwargs):
        contexto = {

        }

        return render(self.request, self.template_name, contexto)


class SaveOrder(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Fechar pedido')


class Detail(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Fechar pedido')


# Create your views here.
