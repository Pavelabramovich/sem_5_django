from datetime import date, timedelta
from django.views import generic
from django.db.models import Model
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .models import \
    Category, \
    Producer, \
    Provider, \
    Product, \
    Buy

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
    return render(request, "shop/home.html", {
        'products': products,
        'providers': providers,
        'producers': producers,
        'buys': buys
    })


class ProductListView(generic.ListView):
    model = Product
    template_name = 'shop/product_list.html'


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'shop/product_details.html'



