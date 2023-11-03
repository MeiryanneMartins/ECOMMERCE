from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages

from product.models import Variation


class Pay(View):
    template_name = 'order/pay.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Você precisa fazer login.'
            )

            return redirect('profile_user:criar')

        if not self.request.session.get('car'):
            messages.error(
                self.request,
                'Carrinho vazio.'
            )

            return redirect('product:list')

        car = self.request.session.get('car')
        car_variations_ids = [v for v in car]
        bd_variations = list(
            Variation.objects.select_related(
                'product').filter(id__in=car_variations_ids)
        )

        for variation in bd_variations:
            vid = variation.id

            stock = variation.stock
            qtd_car = car[vid]['amount']
            price_unit = car[vid]['price']
            price_unit_promo = car[vid]['price_marketing_promotional']

            if stock < qtd_car:
                car[vid]['amount'] = stock
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
