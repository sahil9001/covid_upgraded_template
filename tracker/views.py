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
from . serializer import locationSerializer,extendedUserSerializer,UserSerializer
from datetime import datetime
from django.contrib.auth.models import User
import pytz
from django.utils import timezone
from django.db.models import Q
####firebase
import firebase_admin
from firebase_admin import credentials, firestore,db
import os, sys
import json
import ast
dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
covid = os.path.join(dirname, "covid.json")
cred = credentials.Certificate(covid)
firebase_admin.initialize_app(cred)
db = firestore.client()
###pusher
pusher_client = pusher.Pusher(
  app_id='967595',
  key='c73ea8196f369f3e7364',
  secret='3e271da7d6f8256557c1',
  cluster='ap2',
  ssl=True
)
@api_view(['POST'])
def register(request):
    global db
    serialized = UserSerializer(data = request.data)
    print(request.data['password'])
    data = {}
    my_email = request.data['email']
    my_username = request.data['username']
    my_password = request.data['password']
    if serialized.is_valid():
        user =User.objects.create_user(email= my_email, username= my_username, password =my_password)
        data['sucess'] = "user created"
        channel= "channel" + str(user.id)
        print(channel)
        doc_ref = db.collection(u'main_data').document(channel)
        doc_ref.set({
            u'latitude':None,
            u'longitude':None,
            u'last_fetched': None,
        })
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
    global db
    data = {}
    user = request.user
    serializer = locationSerializer(data= request.data)
    print(request.data)
    if serializer.is_valid():
        last_date = datetime.now()
        new_location = locationDetail(user = user,latitude = request.data['latitude'], longitude = request.data['longitude'],last_fetched = last_date)
        #please manage the server time setting later 
        new_location.save()
        data['success'] = "new location saved"
        channel = "channel"+ str(request.user.id)
        print(channel)
        doc_ref = db.collection(u'main_data').document(channel)
        doc_ref.set({
            u'latitude':new_location.latitude,
            u'longitude':new_location.longitude,
            u'last_fetched': str(last_date),
        })
        pusher_client.trigger(channel, 'my-event', {'latitude': new_location.latitude,'longitude':new_location.longitude,'last_fetch':str(last_date)})
        return Response(data = data ,status= status.HTTP_200_OK)
    return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

def test(request):
    data = []
    all_user = extendedUser.objects.filter(~Q(status = 5))
    my_user = extendedUser.objects.get(user = request.user)
    for extend_user in all_user:
        try:
            location_detail = locationDetail.objects.filter(user = extend_user.user).order_by('-id')[0]
            extend_user_latitude = location_detail.latitude
            extend_user_longitude = location_detail.longitude
            extend_user_last_fetch = location_detail.last_fetched
        except:
            extend_user_latitude = None
            extend_user_longitude = None
            extend_user_last_fetch = None
        user_coordinates = {'channel_id':extend_user.user.id,'status':extend_user.status,'username':extend_user.user.username,'latitude':extend_user_latitude,'longitude':extend_user_longitude,'last_fetch':extend_user_last_fetch}
        print(extend_user.user.username + " id = " +str(extend_user.user.id))
        data.append(user_coordinates)
    try:
        user_location_detail = locationDetail.objects.filter(user = request.user).order_by('-id')[0]
        user_latitude = user_location_detail.longitude
        user_longitude = user_location_detail.latitude
        user_last_fetch = user_location_detail.last_fetched
    except:
        user_latitude = None
        user_longitude = None
        user_last_fetch = None 
    user_coordinates = {'channel_id':request.user.id,'status':my_user.status,'username':request.user.username,'latitude':user_latitude,'longitude':user_longitude,'last_fetch':user_last_fetch}
    all_data = {'global_plotted_coordinates':data,'user_plotted_data':user_coordinates}
    return render(request,'table.html',{'all_data':all_data})
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def table(request):
    data = []
    all_user = extendedUser.objects.filter(~Q(status = 5))
    my_user = extendedUser.objects.get(user = request.user)
    for extend_user in all_user:
        try:
            location_detail = locationDetail.objects.filter(user = extend_user.user).order_by('-id')[0]
            extend_user_latitude = location_detail.latitude
            extend_user_longitude = location_detail.longitude
            extend_user_last_fetch = location_detail.last_fetched
        except:
            extend_user_latitude = None
            extend_user_longitude = None
            extend_user_last_fetch = None
        user_coordinates = {'channel_id':extend_user.user.id,'status':extend_user.status,'username':extend_user.user.username,'latitude':extend_user_latitude,'longitude':extend_user_longitude,'last_fetch':extend_user_last_fetch}
        print(extend_user.user.username + " id = " +str(extend_user.user.id))
        data.append(user_coordinates)
    try:
        user_location_detail = locationDetail.objects.filter(user = request.user).order_by('-id')[0]
        user_latitude = user_location_detail.longitude
        user_longitude = user_location_detail.latitude
        user_last_fetch = user_location_detail.last_fetched
    except:
        user_latitude = None
        user_longitude = None
        user_last_fetch = None 
    user_coordinates = {'channel_id':request.user.id,'status':my_user.status,'username':request.user.username,'latitude':user_latitude,'longitude':user_longitude,'last_fetch':user_last_fetch}
    all_data = {'global_plotted_coordinates':data,'user_plotted_data':user_coordinates}
    return Response(all_data)