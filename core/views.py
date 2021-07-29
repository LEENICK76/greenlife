from django.shortcuts import render


# Create your views here.

def home(request):
    context = {}
    return render(request, 'core/home.html', context=context)


def cart(request):
    context = {}
    return render(request, 'core/cart.html', context=context)


def checkout(request):
    context = {}
    return render(request, 'core/checkout.html', context=context)
