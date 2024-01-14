from django.contrib.auth.models import User
from django.core import serializers

"""
Return a List of all existing Users. All users are saved in json format
"""
def getAllUser():
    global allUsers
    allUsers = User.objects.all()
    listUser = []   
    for allU in allUsers:           
        listUser.append(serializers.serialize('json',[allU,])[1:-1])      
    return listUser 