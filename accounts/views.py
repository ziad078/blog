from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.
@login_required(login_url="login")
def signout(req):
    logout(req)
    return redirect("login")

def register(req):
    if req.user.is_authenticated:
        return redirect('index')
    if req.method == "POST":
        username = req.POST["username"]
        email = req.POST["email"]
        pass1 = req.POST["password"]
        pass2 = req.POST["cpassword"]
        if User.objects.filter(email = email).exists() or  User.objects.filter(username = username).exists():
            messages.warning(req,"This user already exists")
            return redirect('register')
        if pass1 != pass2:
            messages.warning(req,"passwords don't match")
            return redirect('register')
        user = User.objects.create_user(
            username=username,
            email=email,
            password=pass1
        )
        user.save()
        user_login =  authenticate(username = username, password = pass1)
        if user_login:
            login(req,user_login)
            return redirect('user_profile')
        else:
            messages.warning(req,"something went error")
    return render(req,'pages/register.html')
def signin(req):
    next_url = req.POST.get('next') or req.GET.get('next') or '/'
    if req.user.is_authenticated:
        return redirect('index')
    if req.method == "POST":
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(username = username, password=password)
        if user:
            login(req,user)
            return redirect(f"{next_url}")
        else:
            messages.warning(req, "check your credentials")
            return redirect('login')
        
    return render(req,'pages/login.html')



def user_profile(req):
    

    if req.method == "POST":
        user__profile = Profile.objects.get(user = req.user)
        if req.FILES.get('img'):
            img = req.FILES.get('img')
            user__profile.img = img
        name = req.POST.get('name')
        bio = req.POST.get('bio')
        email = req.POST.get('email')
        user__profile.name = name
        user__profile.bio = bio
        req.user.email = email
        req.user.username = name


        req.user.save()
        user__profile.save()
    user__profile = Profile.objects.get(user = req.user)
    context = {
        "name": user__profile.name,
        "bio": user__profile.bio,
        "img": user__profile.img
    }
    return render(req,'pages/profileSettings.html', context)



def delete_profile_img(req):
    user__profile = Profile.objects.get(user = req.user)
    user__profile.img = "photos/blank.jpeg"
    user__profile.save()
    return redirect('user_profile')