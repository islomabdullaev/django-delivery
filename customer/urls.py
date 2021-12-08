from django.urls import path

from customer.views import Index, About, Order, Menu, MenuSearch

app_name = "customer"

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("about/", About.as_view(), name="about"),
    path("order/", Order.as_view(), name="order"),
    path("menu/", Menu.as_view(), name="menu"),
    path("menu/search/", MenuSearch.as_view(), name="menu-search"),
]
