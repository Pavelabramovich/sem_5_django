import requests
from datetime import date, timedelta
from datetime import datetime

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
    Product, Coupon,
    Buy,Review, Provider,
    Profile, News, Faq,
    Category, CarouselItem
)
from .forms import UserProfileCreationForm, RegistrationForm, CreateBuyForm, CreateReviewForm


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


def faqs(request):
    f = Faq.objects.all()

    return render(request, "shop/faqs.html", {
        'faqs': f
    })


def home(request):
    categories = Category.objects.all()
    carousel_items = CarouselItem.objects.all()
  #  carousel_items = list(CarouselItem.objects.all())[-2:-3:-1]
    news = News.objects.order_by('-date')[:3]
    providers = Provider.objects.all()
    coupons = Coupon.objects.all()

    return render(request, "shop/home.html", {
        'categories': categories,
        'carousel_items': carousel_items,
        'news': news,
        'coupons': coupons,
        'providers': providers
    })


def create_buy(request, *, pk):
    product = Product.objects.filter(pk=pk)[0]
    # discount = Coupon.objects.filter(user=request.user)
    #
    # if not discount.exists():
    #     discount = 0
    # else:
    #     discount = discount[0].discount

    discount = 0

    if request.method == 'GET':
        form = CreateBuyForm()
        return render(request, "shop/create_buy.html", {'product': product, 'form': form, 'discount': discount})

    if request.method == 'POST':
        form = CreateBuyForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                buy = form.save(commit=False)

                buy.user = request.user
                buy.product = product
                buy.date = datetime.now()

                buy.save()

                messages.success(request, "You have buy successfully.")
                return redirect(f'shop:category-detail', pk=product.category.pk)
        else:
            return render(request, "shop/create_buy.html", {'product': product, 'form': form, 'discount': discount})


def create_review(request, *, pk):
    product = Product.objects.filter(pk=pk)[0]

    if request.method == 'GET':
        form = CreateReviewForm()
        return render(request, "shop/create_review.html", {'product': product, 'form': form})

    if request.method == 'POST':
        form = CreateReviewForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                user = request.user

                content = form.cleaned_data['content']

                Review.objects.create(
                    user=user,
                    product=product,
                    content=content
                )

                messages.success(request, "You create review successfully.")
                return redirect(f'shop:product-detail', pk=product.pk)
        else:
            return render(request, "shop/create_review.html", {'product': product, 'form': form})


class ProductListView(generic.ListView):
    model = Product
    paginate_by = 10


class ProductDetailView(generic.DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['carousel_items'] = CarouselItem.objects.all()
        return context


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
        form = RegistrationForm()
        return render(request, 'shop/register.html', {'form': form})

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()

                messages.success(request, "You have singed up successfully.")
                login(request, user)
                return redirect('shop:home')
        else:
            return render(request, 'shop/register.html', {'form': form})


class CategoryDetailView(generic.DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['carousel_items'] = CarouselItem.objects.all()
        return context


class NewsDetailView(generic.DetailView):
    model = News


class FaqDetailView(generic.DetailView):
    model = Faq


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'shop/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context
