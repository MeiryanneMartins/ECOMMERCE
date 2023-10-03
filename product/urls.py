from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.ListProduct.as_view(), name="list"),
    path('<slug>', views.DetailProduct.as_view(), name="detail"),
    path('adicionarcarrinho/', views.AddCar.as_view(), name="adicionaraocarrinho"),
    path('removecarrinho/', views.RemoveCart.as_view(), name='removecarrinho'),
    path('carrinho/', views.Cart.as_view(), name='carrinho'),
    path('finalizar/', views.Finish.as_view(), name='finalizar')

]
