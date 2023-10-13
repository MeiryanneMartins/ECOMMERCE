from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models


class ListProduct(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 2


class DetailProduct(DetailView):
    model = models.Product
    template_name = 'product/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class AddCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HHTP_REFERER',
            reverse('product:list')
        )
        variation_id = self.request.GET.get('vid')

        if not variation_id:
            messages.error(
                self.request,
                'Produto não existe'
            )
            return redirect(http_referer)

        variation = get_object_or_404(models.Variation, id=variation_id)

        if not self.request.session.get('car'):
            self.request.session['car'] = {}
            self.request.session.save()

            car = self.request.session['car']

            if variation_id in car:
                # TODO:variação existe no carrinho

                pass
            else:
                # TODO:variação não existe no carrinho
                pass

        return HttpResponse(f'{variation.product} {variation.name}')


class RemoveCart(ListView):
    pass


class Cart(ListView):
    pass


class Finish(ListView):
    pass
