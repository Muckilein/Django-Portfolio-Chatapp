from django.shortcuts import render
from .models import Message
from .models import Chat
from .functions import *
from django.contrib.auth import authenticate,login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth import get_user_model
from django.db.models.fields import DateField
from datetime import date
from django.db import models

allUsers = []


# Create your views here.

"""
Chat page. When noone is logged in it redirects to 'login'.
Creates a new Message when the method is 'POST' and returns it a a json. Otherwise it just
"""
@login_required(login_url='/login/')
def index(request): 
    print(type(request.user))
    if request.method =="POST":             
        chatID = request.POST.get('chatID')
        receiverID = request.POST['receiverID']
        chatIDINT = int(chatID)              
        if chatIDINT == 0:           
           myChat = Chat.objects.create()  
        else:          
           myChat = Chat.objects.get(id = chatID)       
        newMessage = Message.objects.create(text= request.POST['textmessage'], chat = myChat, author = request.user, receiver = User.objects.get(id =receiverID ))
        serializedObj = serializers.serialize('json',[newMessage,])
        return JsonResponse(serializedObj[1:-1],safe=False)     
    return render(request,'chat/index.html',{'username':request.user,'messages':[]})#schaut automatisch im templates Ordner


"""
Log in of the user with the given username and password. If successful it redirects to 'chat'
"""
def login_view(request):
    redirect = request.GET.get('next')
    if redirect is None:
        redirect = '/chat/'        
    print(redirect)
    if request.method =="POST":
        print('Post request')
        username = request.POST.get('username') #beide Varianten gehen
        password = request.POST['password']      
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            print('logged in')
            return HttpResponseRedirect(request.POST.get('redirect'))
        else:
             return render(request,'auth/login.html',{'wrongpassword':True,'redirect':redirect})            
    return render(request,'auth/login.html',{'redirect':redirect})

"""
Loggout of the logged in user
"""
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')

"""
Registers a new User with the given user name and password. The firstname will be set to the username with the first letter capitalized
"""
def registerView(request):
     if request.method =="POST":
        print('Post request')
        username = request.POST.get('username') #beide Varianten gehen
        password = request.POST['password'] 
        password2 = request.POST['password2'] 
        print('pw', password)
        if password == password2:
           print('password are equal')
           user=User.objects.create_user(username, "test@mail", password)
           user.first_name = username.capitalize();
           user.save()        
           return HttpResponseRedirect('/login/')
        else:
             print('passwords are not equal')
     return render(request,'auth/register.html')
 
"""
Send a Json containing the List of all registered Users back
They are stored in 'users'
"""
def allUser(request):    
    listUser = getAllUser()     
    return JsonResponse({"users":listUser},safe=False)   

"""
Send a Json containing the List of all registered Messages between the logged in user and the given chatpartner back
They are stored in 'messages'
"""
def chatList(request): 
    authorID = request.user.id  
    print("Call chatList", authorID)   
    if request.method =="POST":      
       reID = request.POST.get('receiverID')           
       chatMessages = Message.objects.filter(receiver__id = reID , author__id = authorID) |  Message.objects.filter(receiver__id = authorID , author__id = reID)
       chatMessages = chatMessages.order_by("pk")
       messages =[]
       for mes in chatMessages:
         m= serializers.serialize('json',[mes,])[1:-1]          
         messages.append(m)
       return JsonResponse({"messages":messages},safe=False)      
    return render(request,'chat/index.html')
    
    
    
 