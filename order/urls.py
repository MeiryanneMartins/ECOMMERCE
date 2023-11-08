from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path('pagar/<int:pk>', views.Pay.as_view(), name="pagar"),
    path('salvarpedido/', views.SaveOrder.as_view(), name="salvarpedido"),
    path('list/', views.List.as_view(), name="list"),
    path('detalhe/<int:pk>', views.Detail.as_view(), name="detalhe")

]
