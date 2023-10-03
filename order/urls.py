from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path('', views.Pay.as_view(), name="pagar"),
    path('fecharpedido/', views.CloseOrder.as_view(), name="fecharpedido"),
    path('detalhe/', views.Detail.as_view(), name="detalhe")

]
