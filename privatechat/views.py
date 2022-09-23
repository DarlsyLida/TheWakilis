from email import message
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import ChatModel
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from .models import *
from django.contrib import messages



def register(request):
    if request.method=="POST":   
        username = request.POST['username']
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')
        
        user = User.objects.create_user(username, email, password1)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return redirect('login')   
    return render(request, "register.html")

def login_page(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials")
            return render(request, "login.html")
        # return render(request, 'blog.html')   
    return render(request, "login.html")



def private_chat_home(request):
    users = User.objects.exclude(username=request.user.username)

    return render(request, 'chat.html', context={'users': users})

def chatPage(request, username):
    user_obj = User.objects.get(username=username)
    users = User.objects.exclude(username=request.user.username)
    if request.user.is_authenticated:

        if request.user.id > user_obj.id:
            thread_name = f'chat_{request.user.id}-{user_obj.id}'
        else:
            thread_name = f'chat_{user_obj.id}-{request.user.id}'
        message_objs = ChatModel.objects.filter(thread_name=thread_name)
        senders = {}
        send_messg = []
        for i, mesg in enumerate(message_objs):
            user_obj_temp = User.objects.get(id=mesg.sender)
            senders[user_obj_temp.id] = f"{user_obj_temp.username}"
            send_messg.append([f"{mesg.sender}", f"{mesg.message}", mesg.timestamp])
        return render(request, 'message.html', context={'user' : f"{user_obj.id}" ,'users': users, 'messages' : send_messg, 'username' : username, 'count' : len(send_messg)})
    else:
        return render(request, 'chat.html')