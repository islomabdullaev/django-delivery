from django.urls import path

from restaurant.views import Dashboard

app_name = "restaurant"

urlpatterns = [
    path("dashboard/", Dashboard.as_view(), name="dashboard")
]
