from datetime import date, timedelta
from django.views import View
from django.views import generic
from django.db.models import Model
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .forms import LoginForm, RegisterForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from .models import \
    Category, \
    Producer, \
    Provider, \
    Product, \
    Buy, \
    Profile

import requests


def get_weather():
    appid = '91d45fb3f775b8f850579a41205a2a39'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    city = 'Minsk'
    res = requests.get(url.format(city)).json()

    return res["main"]["temp"]


def get_bitcoin():
    datetime_today = date.today()
    date_today = str(datetime_today)
    date_yesterday = str(datetime_today - timedelta(days=1))

    api = 'https://api.coindesk.com/v1/bpi/currentprice.json?start=' \
          + date_yesterday + '&end=' + date_today + '&index=[USD]'

    response = requests.get(api, timeout=2)
    response.raise_for_status()
    prices = response.json()
    btc_price = prices.get("bpi")["USD"]["rate"]

    return btc_price


def index(request):

    sort = request.GET.getlist('sort')

    products = Product.objects.all().order_by(*sort)
    buys = Buy.objects.all()
    providers = Provider.objects.all()

    return render(request, "index.html", {
        "products": products,
        "providers": providers,
        "buys": buys,
        "temp": get_weather(),
        "bitc": get_bitcoin(),
    })


def home(request):
    products = Product.objects.all()
    providers = Provider.objects.all()
    producers = Producer.objects.all()
    buys = Buy.objects.all()
    return render(request, "shop_app/home.html", {
        'products': products,
        'providers': providers,
        'producers': producers,
        'buys': buys
    })


class ProductListView(generic.ListView):
    model = Product
    paginate_by = 10


class ProductDetailView(generic.DetailView):
    model = Product


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = "shop_app/login.html"

    def get_success_url(self):
        return reverse_lazy('shop:home')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'shop_app/register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()

                Profile.objects.create(
                    user=user,
                    phone=form.cleaned_data['phone'],
                    address=form.cleaned_data['address']
                ).save()

                messages.success(request, "You have singed up successfully.")
                login(request, user)
                return redirect('shop:home')
        else:
            return render(request, 'shop_app/register.html', {'form': form})
