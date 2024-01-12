from django.contrib.auth.models import User
from django.core import serializers

def getAllUser():
    global allUsers
    allUsers=User.objects.all()
    listUser =[]   
    for allU in allUsers:           
        listUser.append(serializers.serialize('json',[allU,])[1:-1])      
    return listUser 