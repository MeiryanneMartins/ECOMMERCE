from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages

from product.models import Variation
from .models import Order, ItemOrder

from utils import utils


class Pay(DetailView):
    template_name = 'order/pay.html'
    model = Order
    pk_url_kwarg = 'pk'
    context_object_name = 'order'


class SaveOrder(View):
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
            vid = str(variation.id)

            stock = variation.stock
            qtd_car = car[vid]['amount']
            price_unit = car[vid]['price_amount']
            price_unit_promo = car[vid]['price_amount_promotional']

            if stock < qtd_car:
                car[vid]['amount'] = stock
                car[vid]['price_amount'] = stock * price_unit
                car[vid]['price_amount_promotional'] = stock * \
                    price_unit_promo

                messages.error(
                    self.request,
                    'Estoque insuficiente.'
                )

                self.request.session.save()
                return redirect('product:car')

        total_amount_car = utils.cart_total_qtd(car)
        value_total_car = utils.cart_totals(car)

        order = Order(
            user=self.request.user,
            total_amount=value_total_car,
            sum_order=total_amount_car,
            status='C',
        )

        order.save()
        ItemOrder.objects.bulk_create(
            [
                ItemOrder(
                    order=order,
                    product=v['product_name'],
                    product_id=v['product_id'],
                    variation=v['variation_name'],
                    variation_id=v['variation_id'],
                    price=v['price_amount'],
                    price_promotional=v['price_amount_promotional'],
                    amount=v['amount'],
                    image=v['image'],

                ) for v in car.values()
            ]
        )

        del self.request.session['car']
        return redirect(
            reverse(
                'order:pay.html',
                kwargs={
                    'pk': order.pk
                }
            )
        )

        return render(self.request, self.template_name, contexto)


class Detail(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Fechar pedido')


class List(View):
    def get(self, *args, **kwargs):
        return HttpResponse('List')


# Create your views here.
