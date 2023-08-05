from django.urls import path, re_path
from . import views
from django.contrib.auth.views import LogoutView


app_name = 'shop'


urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.ProductListView.as_view(), name='products'),
    re_path(r'product/(?P<pk>.+)/$', views.ProductDetailView.as_view(), name='product-detail'),

    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='shop:home'), name='logout'),
    path('register/', views.register, name='register'),
]
