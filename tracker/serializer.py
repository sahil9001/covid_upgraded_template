from rest_framework import serializers
from . models import locationDetail
from accounts.models import extendedUser
from django.contrib.auth.models import User
class locationSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='username'
    )
    class Meta:
        model = locationDetail
        fields = ('user','latitude','longitude','id','last_fetched')
        read_only_fields = ('id','last_fetched')  
class extendedUserSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='username'
    )
    class Meta:
        model = locationDetail
        fields = ('user','status','id')   
        read_only_fields = ('id')   
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password','first_name','last_name','email','id')
        write_only_fields = ('password',)
        read_only_fields = ('id',)