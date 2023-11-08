from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.ListProduct.as_view(), name="list"),
    path('<slug>', views.DetailProduct.as_view(), name="detail"),
    path('adicionarcarrinho/', views.AddCart.as_view(),
         name="adicionaraocarrinho"),
    path('removerdocarrinho/', views.RemoveCart.as_view(),
         name="removerdocarrinho"),
    path('carrinho/', views.Car.as_view(), name='carrinho'),
    path('finalizar/', views.Finish.as_view(), name='finalizar'),
    path('busca/', views.Search.as_view(), name="busca"),

]
