import requests
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.views import generic
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login

from .models import (
    Product,
    Buy,
    Profile,
    Category
)
from .forms import RegisterForm


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


def home(request):
    categories = Category.objects.all()

    return render(request, "shop/home.html", {
        'categories': categories
    })


class ProductListView(generic.ListView):
    model = Product
    paginate_by = 10


class ProductDetailView(generic.DetailView):
    model = Product


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = "shop/login.html"

    def get_success_url(self):
        return reverse_lazy('shop:home')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'shop/register.html', {'form': form})

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
            return render(request, 'shop/register.html', {'form': form})


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'shop/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context
