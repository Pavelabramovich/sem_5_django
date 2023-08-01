from django.urls import path, re_path
from . import views


app_name = 'shop'


urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.ProductListView.as_view(), name='products'),
    re_path(r'product/(?P<pk>.+)/$', views.ProductDetailView.as_view(), name='book-detail'),

    path('', views.index),
]
