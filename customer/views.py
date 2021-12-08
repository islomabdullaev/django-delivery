from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from .models import MenuItem, Category, OrderModel


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
        entres = MenuItem.objects.filter(category__name__contains='Entre')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        # pass into context
        context = {
            'appetizers': appetizers,
            'entres': entres,
            'desserts': desserts,
            'drinks': drinks,
        }

        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        email = request.POST.get("email")
        street = request.POST.get("street")
        city = request.POST.get("city")
        phone = request.POST.get("phone")
        zip_code = request.POST.get("zip_code")

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

        price = 0
        item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            phone=phone,
            zip_code=zip_code
        )
        order.items.add(*item_ids)

        message = (
            "Thank you for your order ! Your food is being prepared and will be ordered soon ! \n"
            f"f'Total Price: ${price}'"
        )

        send_mail(
            "Thank You For Your Order !",
            message,
            "example@example.com",
            [email],
            fail_silently=False,
        )

        context = {
            'items': order_items['items'],
            'price': price
        }

        return render(request, 'customer/order_confirmation.html', context)


class Menu(View):
    def get(self, request, *args, **kwargs):
        menu = MenuItem.objects.all()

        context = {
            "menu_items": menu,
        }

        return render(request, "customer/menu.html", context)


class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        q = self.request.GET.get("q")
        menu = MenuItem.objects.filter(
                Q(name__icontains=q) | Q(price__icontains=q) | Q(description__icontains=q)
            )
        context = {
            "menu_items": menu,
        }
        return render(request, "customer/menu.html", context)
