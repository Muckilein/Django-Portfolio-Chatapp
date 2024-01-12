from django.shortcuts import render
from .models import Message
from .models import Chat
from .functions import *
from django.contrib.auth import authenticate,login
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
@login_required(login_url='/login/')
def index(request): 
    print(type(request.user))
    if request.method =="POST":
        print('received data ' + request.POST['textmessage'])        
        chatID = request.POST.get('chatID')
        receiverID = request.POST['receiverID']
        chatIDINT = int(chatID) 
        print(type(chatID)) 
        print('id ist ' + chatID)        
        if chatIDINT == 0:           
           myChat = Chat.objects.create()  
        else:
           print("else")
           myChat = Chat.objects.get(id = chatID)
        print("new Message")
        newMessage = Message.objects.create(text= request.POST['textmessage'], chat = myChat, author = request.user, receiver = User.objects.get(id =receiverID ))
        serializedObj = serializers.serialize('json',[newMessage,])
        return JsonResponse(serializedObj[1:-1],safe=False)     
    return render(request,'chat/index.html',{'username':request.user,'messages':[]})#schaut automatisch im templates Ordner

def loginView(request):
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

def registerView(request):
     if request.method =="POST":
        print('Post request')
        username = request.POST.get('username') #beide Varianten gehen
        password = request.POST['password'] 
        password2 = request.POST['password2'] 
        print('pw', password)
        if password == password2:
           print('password are equal')
           User.objects.create_user(username, "test@mail", password)       
           return HttpResponseRedirect('/login/')
        else:
             print('passwords are not equal')
     return render(request,'auth/register.html')

def allUser(request):    
    listUser = getAllUser()     
    return JsonResponse({"users":listUser},safe=False)   


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
    #    userList =  getAllUser();   
       return JsonResponse({"messages":messages},safe=False)
    print('weiter')   
    return render(request,'chat/index.html')
    
    
    
 