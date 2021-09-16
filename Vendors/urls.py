from django.urls import path

from Vendors import views

urlpatterns = [
    path('admin-farmer/', views.admin_farmer, name='admin-farmer'),
    path('become-farmer/', views.become_farmer, name='become-farmer'),
    path('add-product/', views.add_product, name='add_product'),

]
