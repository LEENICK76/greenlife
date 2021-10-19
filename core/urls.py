from django.urls import path

from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.update_item, name='update_item'),
    path('process_order/', views.process_order, name='process_order'),
    path('search', views.search, name='search'),
    path('about/', views.about_us, name='about'),
]
