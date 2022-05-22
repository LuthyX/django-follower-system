from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.contrib import messages
import requests

from follow.models import FollowersCount


# Create your views here.
def index(request):
    logged_in_user = request.user.username
    current_user = request.GET.get('user')
    if current_user == None:
        current_user = logged_in_user
        
    logged_in_user = request.user.username
    user_followers = len(FollowersCount.objects.filter(user = current_user))
    user_following = len(FollowersCount.objects.filter(follower = current_user))
    user_followers0 =  FollowersCount.objects.filter(user = current_user)
    user_followers1= []
    for i in user_followers0:
        user_followers0 = i.follower
        user_followers1.append(user_followers0)
    if logged_in_user in user_followers1:
        follow_button_value = 'unfollow'
    else:
        follow_button_value = 'follow' 

    return render(request, 'index.html', {
        'user_followers' : user_followers,
        'user_following' : user_following,
        'current_user': current_user,
        'follow_button_value':follow_button_value})

def followers_count(request):
    if request.method == 'POST':
        value = request.POST['value']
        user = request.POST['user']
        follower = request.POST['follower']
        if value == 'follow':
            followers_cnt = FollowersCount.objects.create(follower = follower, user= user)
            followers_cnt.save()
        else:
            followers_cnt = FollowersCount.objects.get(follower = follower, user =user)
            followers_cnt.delete()
        return redirect('/?user='+user)

def register(request):
    if request.method == 'POST':
        username =  request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('register')
            else:
                user= User.objects.create_user(username = username, email = email, password = password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('register')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username = username, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return redirect('login')    
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

