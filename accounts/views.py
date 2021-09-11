from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your views here.
from Products.models import Seller
from accounts.forms import RegisterForm, LoginForm
from core.models import Customer


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            number = form.cleaned_data['number']
            email = form.cleaned_data['email']
            account = form.cleaned_data['account_type']
            if account == 'CUSTOMER':
                Customer.objects.create(
                    name=username,
                    number=number,
                    email=email,
                    user=user
                )
            elif account == 'FARMER':
                Seller.objects.create(
                    name=username,
                    number=number,
                    email=email,
                    user=user
                )

            messages.success(request, f'Account for {username} was created successfully')

            print(form)
            return redirect('login')
    context = {'form': form}
    return render(request, 'auth/register.html', context=context)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get['username']
        password = request.POST.get['password']

        user = authenticate(request, password=password, username=username)
        if user is not None:
            if user.is_active:
                login(request, user)
                redirect('home')
            else:
                messages.warning(request, 'Your account is disabled, contact us for support')
        else:
            messages.info(request, 'Either your password or email is incorrect')
    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    redirect('login')
