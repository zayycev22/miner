from django.shortcuts import render, redirect
from .models import ExUser, PC, Tokens
from django.contrib.auth import login, logout, authenticate
from .CustomBackend import CustomBackendModel
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')


def login_p(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        token = request.POST.get('token')
        user = authenticate(username=username, password=password, token=token)
        if user is not None:
            login(request, user)
            return redirect(f"/User/{user.username}")

        else:
            print("Auth problem")
            print(username)
            print(password)
            return redirect("/")


def log_out(request):
    logout(request)
    return redirect('/')


@login_required(redirect_field_name='login')
def user_page(request, name):
    user = ExUser.objects.get(username=name)
    if user is not None:
        return render(request, 'user_page.html', {"user_info": user})
    else:
        return HttpResponse(status=404)


def work_dirs(request):
    computers = PC.objects.filter(token=request.user.token)
    if len(computers) > 0:
        return render(request, "wordirectory.html", {"computers": computers})
    else:
        return HttpResponse(404)


def workdir_info(request, name):
    computers = PC.objects.get(name=name, token=request.user)  # по user.id
    if computers is not None:
        return render(request, "workdir_info.html", {"computer": computers})
    else:
        return HttpResponse("Bad request")


def add_workdir(request, name):
    computers = PC.objects.get(name=name)


def change_status(request, name):
    computers = PC.objects.get(name=name)
    if request.method == 'POST' and request.user.token == computers.user.token:
        if computers.is_active is True:
            computers.is_active = False
            computers.save()
        else:
            computers.is_active = True
            computers.save()
        return redirect('workdir')
    else:
        return HttpResponse(504)
