from django.http.response import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.contrib.auth import get_user,authenticate,login
from django.template import RequestContext

# Create your views here.
def LoginView(request):
    if request.method =="GET":
        return render(request,"login.html")
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return redirect("login")

def IndexView(request):
    return redirect("home")

def HomeView(request):
    if request.method =="GET":
        user = get_user(request)
        if user.is_anonymous:
            return redirect("login")
        else:
            return render(request,"home.html")
    if request.method == "POST":
        return HttpResponseNotFound("")
        
