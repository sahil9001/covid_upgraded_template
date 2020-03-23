from django.shortcuts import render
from django.http import HttpResponse
from accounts.models import extendedUser
from . models import locationDetail
import pusher
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from . serializer import *
from datetime import datetime
from django.contrib.auth.models import User
import pytz
from django.utils import timezone
from django.db.models import Q

pusher_client = pusher.Pusher(
  app_id='967595',
  key='c73ea8196f369f3e7364',
  secret='3e271da7d6f8256557c1',
  cluster='ap2',
  ssl=True
)
@api_view(['POST'])
def register(request):
    serialized = UserSerializer(data = request.data)
    print(request.data['password'])
    data = {}
    my_email = request.data['email']
    my_username = request.data['username']
    my_password = request.data['password']
    if serialized.is_valid():
        user =User.objects.create_user(email= my_email, username= my_username, password =my_password)
        my_extended_user = extendedUser(user = user)
        my_extended_user.save()
        data['sucess'] = "user created"
        return Response(data = data ,status= status.HTTP_200_OK)
    return Response(serialized.errors, status= status.HTTP_400_BAD_REQUEST)
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def updateUserDetail(request):
    my_extend_user = extendedUser.objects.get(user = request.user)
    print(my_extend_user.user.username)
    data = {}
    try:
        my_extend_user.status = int(request.data['user_status_choices'])
        print(str(my_extend_user.user_status_choices) + "changed")
        my_extend_user.save()
        data['success'] = "updated successfully"
        print(my_extend_user.status)
        return Response(data = data, status= status.HTTP_200_OK)
    except:
        data['error'] = "Data for user status missing most probably"
        return Response(data = data, status= status.HTTP_400_BAD_REQUEST)

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def inputLocation(request):
    data = {}
    user = request.user
    serializer = locationSerializer(data= request.data)
    print(request.data)
    if serializer.is_valid():
        new_location = locationDetail(user = user,latitude = request.data['latitude'], longitude = request.data['longitude'],last_fetched = datetime.now())
        #please manage the server time setting later 
        new_location.save()
        data['sucess'] = "new location saved"
        channel = "channel"+ str(request.user.id)
        print(channel)
        pusher_client.trigger(channel, 'my-event', {'latitude': new_location.latitude,'longitude':new_location.longitude})
        return Response(data = data ,status= status.HTTP_200_OK)
    return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
def test(request):
    return render(request,'table.html')
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def table(request):
    data = []
    all_user = extendedUser.objects.filter(~Q(status = 5))
    my_user = extendedUser.objects.get(user = request.user)
    for extend_user in all_user:
        user_coordinates = {'channel_id':extend_user.user.id,'status':extend_user.status,'username':extend_user.user.username}
        print(extend_user.user.username + " id = " +str(extend_user.user.id))
        data.append(user_coordinates)
    all_data = {'global_plotted_coordinates':data}
    return Response(all_data)
