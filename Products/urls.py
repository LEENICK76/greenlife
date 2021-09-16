from django.urls import path
from Vendors import views

urlpatterns = [
    path('customer-requests/', views.my_requests, name='my-request'),
    path('add-requests/', views.make_product_request, name='add-request'),
]