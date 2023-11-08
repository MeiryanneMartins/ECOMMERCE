from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages

from profile_user.models import ProfileUser
from . import models


class ListProduct(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 10
    ordering = ['-id']


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
        variation_stock = variation.stock
        print(f'meu estoque: {variation_stock}')

        product = variation.product
        product_id = product.id
        product_name = product.name
        variation_name = variation.name or ''
        price_unit = variation.price
        print(price_unit)
        price_unit_promotional = variation.price_marketing_promotional
        print(price_unit_promotional)
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
        print(car)

        if variation_id in car:
            amount_car = car[variation_id]['amount']
            amount_car += 1

            if variation_stock < amount_car:
                messages.warning(
                    self.request,
                    f'estoque insuficiente para {amount_car}x no'
                    f'produto "{product_name}". Adicionamos {variation.stock}x'
                    f'no seu carrinho.'
                )

                amount_car = variation_stock
            car[variation_id]['amount'] = amount_car
            car[variation_id]['price_amount'] = price_unit * \
                amount_car
            car[variation_id]['price_amount_promotional'] = price_unit_promotional * \
                amount_car
        else:
            car[variation_id] = {
                'product_id': product_id,
                'product_name': product_name,
                'variation_name': variation_name,
                'variation_id': variation_id,
                'price_unit': price_unit,
                'price_unit_promotional': price_unit_promotional,
                'price_amount': price_unit_promotional,
                'price_amount_promotional': price_unit_promotional,
                'amount': 1,
                'slug': slug,
                'image': image,

            }
        self.request.session.save()

        messages.success(
            self.request,
            f'Produto {product_name} {variation_name} adicionado ao seu '
            f'carrinho {car[variation_id]["amount"]}x.'
        )
        # pprint(car[variation_id])
        return redirect(http_referer)


class RemoveCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('product:list')
        )
        variation_id = self.request.GET.get('vid')

        if not variation_id:
            return redirect(http_referer)

        if not self.request.session.get('car'):
            return redirect(http_referer)

        if variation_id not in self.request.session['car']:
            return redirect(http_referer)

        car = self.request.session['car'][variation_id]

        messages.success(
            self.request,
            f'Produto {car["product_name"]} {car["variation_name"]} '
            f'removido do seu carrinho.'
        )

        del self.request.session['car'][variation_id]
        self.request.session.save()
        return redirect(http_referer)


class Car(View):
    def get(self, *args, **kwargs):
        contexto = {
            'car': self.request.session.get('car', {})
        }
        return render(self.request, 'product/car.html', contexto)


class Finish(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('profile_user:criar')

        profile = ProfileUser.objects.filter(user=self.request.user).exists()

        if not profile:
            messages.error(
                self.request,
                'Usuário sem perfil.'
            )
            return redirect('profile_user:criar')

        if not self.request.session.get('car'):
            messages.error(
                self.request,
                'Carrinho vazio.'
            )
            return redirect('product:list')

        contexto = {
            'user': self.request.user,
            'car': self.request.session['car'],
        }

        return render(self.request, 'product/finish.html', contexto)
