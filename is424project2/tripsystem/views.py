from django.shortcuts import render,redirect
from django import forms
from django.http import HttpResponse
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
                if username == "admin":
                    return redirect("displayAdmin")
                else:
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
def displayAdmin(request):
    if request.method == 'POST':
        choice = request.POST.get('choice')

        if choice == 'add':

            return redirect("addTrip")
        elif choice == 'modify':
            return redirect("modifyTrip")

        elif choice == 'remove':

            return redirect("removeTrip")

    else:
        return render(request,"adminMain.html")

def addTrip(request):
    if request.method == "POST" and request.session["username"] == "admin":
        form = newTripForm(request.POST)
        if form.is_valid():
            source = form.cleaned_data["source"]
            destination = form.cleaned_data["destination"]
            time = form.cleaned_data["time"]
            seats = form.cleaned_data["capacityLeft"]
            new_trip = Trip.objects.create(source=source, destination=destination, time=time, capacityLeft=seats)
            new_trip.save()
            return render(request,"adminAdd.html",{"form":newTripForm(),"message":"Trip added successfully"})
    else:
        return render(request,"adminAdd.html",{"form":newTripForm()})

def modifyTrip(request):
    if request.method == "POST" and request.session["username"] == "admin":
        form = newModifyTripForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data["id"]
            try:
                trip = Trip.objects.get(id=id)

                source = form.cleaned_data["source"]
                destination = form.cleaned_data["destination"]
                time = form.cleaned_data["time"]
                seats = form.cleaned_data["capacityLeft"]
                trip.source = source
                trip.destination = destination
                trip.time = time
                trip.capacityLeft = seats
                trip.save()
                return render(request, "adminModify.html", {"form": newModifyTripForm(), "trips": Trip.objects.all(),"message": "Trip modified successfully"})
            except Exception:
                return render(request, "adminModify.html",
                              {"form": form, "trips": Trip.objects.all(),"message": "Trip id doesnt exists!"})

    else:
        return render(request, "adminModify.html", {"form": newModifyTripForm(),"trips": Trip.objects.all()})

def removeTrip(request):
    if request.method == "POST":
        trip_id = request.POST.get("id")

        try:
            trip = Trip.objects.get(id=trip_id)
            trip.delete()
            return render(request, "adminRemove.html", {"trips": Trip.objects.all(),
                                                        "message": "Trip removed successfully"})
        except Exception:
            return render(request, "adminRemove.html", {"trips": Trip.objects.all(),
                                                        "message": "Trip doesnt exist!"})
    else:
        return render(request, "adminRemove.html", {"trips": Trip.objects.all()})

class newLoginForm(forms.Form):
    username= forms.CharField(label="Username")
    password = forms.CharField(label="Password (8 characters atleast)",widget=forms.PasswordInput)
class newTripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['source', 'destination',"time","capacityLeft"]
class newModifyTripForm(forms.Form):
    id = forms.IntegerField(label="ID")
    source = forms.CharField(label="Source")
    destination = forms.CharField(label="Destination")
    time = forms.CharField(label="Time")
    capacityLeft = forms.CharField(label="Capacity")