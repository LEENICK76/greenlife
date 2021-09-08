from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your views here.
from accounts.forms import RegisterForm
from core.models import Customer


def login(request):

    return render(request, 'auth/login.html')


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            name = form.cleaned_data['name']
            number = form.cleaned_data['number']
            email = form.cleaned_data['email']
            Customer.objects.create(
                name=name,
                number=number,
                email=email,
                user=user
            )

            print(form)
            return redirect('login')
    context = {'form': form}
    return render(request, 'auth/register.html', context=context)
