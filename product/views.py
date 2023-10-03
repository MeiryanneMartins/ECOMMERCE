from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View


class ListProduct(ListView):
    pass


class DetailProduct(ListView):
    pass


class AddCart(ListView):
    pass


class RemoveCar(ListView):
    pass


class Cart(ListView):
    pass


class Finish(ListView):
    pass
