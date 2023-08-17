from django.urls import path, re_path
from django.contrib.auth.views import LogoutView

from . import views
from . import forms


app_name = 'shop'


urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.ProductListView.as_view(), name='products'),
    re_path(r'product/(?P<pk>.+)/$', views.ProductDetailView.as_view(), name='product-detail'),

    path('login/', views.CustomLoginView.as_view(authentication_form=forms.LoginForm), name='login'),
    path('logout/', LogoutView.as_view(next_page='shop:home'), name='logout'),
    path('register/', views.register, name='register'),

    path('user_profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='user-profile')
]

# Admin overriding
# urlpatterns += [
#     path('admin/login/', views.AdminLoginView.as_view(authentication_form=forms.LoginForm)),
# ]

