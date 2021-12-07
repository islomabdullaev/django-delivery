from django.urls import path

from customer.views import Index, About, Order

app_name = "customer"

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("about/", About.as_view(), name="about"),
    path("order/", Order.as_view(), name="order"),
]
