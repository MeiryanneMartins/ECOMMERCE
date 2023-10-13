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
        if self.request.session.get('car'):
            del self.request.session['car']
            self.request.session.save()
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
        product = variation.product
        variation_stock = variation.stock

        product_id = product.id
        product_name = product.name
        variation_name = variation.name or ''
        price_marketing_promotional = variation.price_marketing_promotional
        price = variation.price
        amount = 1
        slug = product.slug
        image = product.image

        if image:
            image = image.name
        else:
            image = ''

        if variation.stock < 1:
            messages.error(
                self.request,
                'Estoque insuficiente'
            )

            return redirect(http_referer)

        if not self.request.session.get('car'):
            self.request.session['car'] = {}
            self.request.session.save()

            car = self.request.session['car']

            if variation_id in car:
                amount_car = car[variation_id]['amount']
                amount_car += 1

                if variation_stock < amount_car:
                    messages.warning(
                        self.request,
                        f'Estoque insuficiente para {amount_car}x no'
                        f'produto "{product.name}". Adicionamos {variation_stock}x'
                        f'no seu carrinho.'
                    )

                    amount_car = variation_stock

                    car[variation_id]['amount'] = amount_car
                    car[variation_id]['price'] = price *\
                        amount_car
                    car[variation_id]['price_marketing_promotional'] = price_marketing_promotional *\
                        amount_car

            else:
                car[variation_id] = {
                    'product_id': product_id,
                    'product_name': product_name,
                    'variation_name': variation_name,
                    'variation_id': variation_id,
                    'price': price,
                    'price_marketing_promotional': price_marketing_promotional,
                    'amount': amount,
                    'slug': slug,
                    'image': image,
                }

                self.request.session.save()

                messages.success(
                    self.request,
                    f'Produto{product_name} {variation_name} adicionado ao seu'
                    f'carrinho {car[variation_id]["amount"]}x.'
                )

                return redirect(http_referer)

        return HttpResponse(f'{variation.product} {variation.name}')


class RemoveCart(View):
    pass


class Cart(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'product/car.html')


class Finish(View):
    pass
