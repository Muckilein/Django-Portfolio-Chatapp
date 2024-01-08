from django.shortcuts import render
from .models import Message
from .models import Chat
from django.contrib.auth import authenticate,login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth import get_user_model

# Create your views here.
@login_required(login_url='/login/')
def index(request):   
    if request.method =="POST":
        print('received data ' + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        newMessage = Message.objects.create(text= request.POST['textmessage'], chat = myChat, author = request.user, receiver = request.user)
        serializedObj = serializers.serialize('json',[newMessage,])
        return JsonResponse(serializedObj[1:-1],safe=False)
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request,'chat/index.html',{'username':request.user,'messages':chatMessages})#schaut automatisch im templates Ordner

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
           user = User.objects.create_user(username, "test@mail", password)
        #    user.last_name = "Lennon"
        #    user.save()
           return HttpResponseRedirect('/login/')
        else:
             print('passwords are not equal')
     return render(request,'auth/register.html')

def jsonView(request):
    user =  User.objects.get(id=1)
    # allUsers = list( User.objects.values())
    allUsers=User.objects.all()
    # print(allUsers[0]) 
    print(type(allUsers[0]))
    print(type(user))
    listUser =[]   
    for allU in allUsers:
        # listUser.append(allU['first_name']) 
        # print(allU)  
        listUser.append(serializers.serialize('json',[allU,])[1:-1])        
       
    # serializedObj = serializers.serialize('json',[listUser,]) 
    # serializedUser= serializers.serialize('json',[user,])[1:-1]
    return JsonResponse({"users":listUser},safe=False)
    
    
 