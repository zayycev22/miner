from django.shortcuts import render, redirect
from .models import ExUser
from django.contrib import auth
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "index.html")


def login_p(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        token = request.POST.get('token')
        user = auth.authenticate(username=username, password=password, token=token)

        if user is not None:
            auth.login(request, user)
            return redirect("/User")

        else:
            print("Auth problem")
            return redirect("/")


def user_page(request, name):
    user = ExUser.objects.get(username=name)
    if user is not None:
        return render(request, 'user_page.html', {"user_info": user})
    else:
        return HttpResponse(status=404)
