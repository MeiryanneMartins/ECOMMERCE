from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from . import models


class ListProduct(ListView):
    model = models.Product
    template_name = 'product/list.html'


class DetailProduct(ListView):
    pass


class AddCart(ListView):
    pass


class RemoveCart(ListView):
    pass


class Cart(ListView):
    pass


class Finish(ListView):
    pass
