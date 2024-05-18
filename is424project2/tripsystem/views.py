from django.shortcuts import render
from django import forms
from .models import *
# Create your views here.
def login(request):
    return render(request,'login.html',{"form":newLoginForm()})


def register(request):

    if request.method == 'POST':

        form = newLoginForm(request.POST)
        if form.is_valid():


            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            if User.objects.filter(username=username).exists() or len(password) < 8:
                return render(request, "register.html",
                              {"form": form,"message": "username exists, or password less than 8 characters!"})

            else:
                new_account = User(username=username, password=password)
                new_account.save()
                return render(request, "login.html",
                              {"form": newLoginForm()})
    else:
        return render(request, "register.html",
                      {"form":newLoginForm()})

def validate_login(request):
    if request.method == 'POST':

        form = newLoginForm(request.POST)
        if form.is_valid():


            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            if User.objects.filter(username=username ,password=password).exists():
                request.session["username"] = username
                return displayBusses(request)

            else:
                return render(request, "login.html",
                              {"form": form,"message":"Username or password wrong"})

def displayBusses(request):

    return render(request, "busses.html",
                  {"trips": Trip.objects.all()})

def displayBus(request,id):
    message =''
    trip = Trip.objects.get(id=id)
    if request.method == 'POST':
        if trip.capacityLeft >0:
            user = User.objects.get(username = request.session.get("username"))
            if user not in trip.users.all():
                trip.users.add(user)
                trip.capacityLeft = trip.capacityLeft-1
                trip.save()
                message = "You have reserved the trip successfully!"
            else:
                trip.users.remove(user)
                trip.capacityLeft =  trip.capacityLeft+1
                trip.save()
                message = "You have been removed from the trip successfully!"
        else:
            message ="Trip has no seats avaliable, sorry!"

    return render(request,"bus.html",{"trip":trip,"message":message})

class newLoginForm(forms.Form):
    username= forms.CharField(label="Username")
    password = forms.CharField(label="Password (8 characters atleast)",widget=forms.PasswordInput)