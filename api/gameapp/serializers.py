from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile,Game,Table,Player



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password','first_name','last_name','email']

    def create(self, validated_data):
        username = validated_data['username']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        password = validated_data['password']
        new_user = User(username=username,first_name=first_name,last_name=last_name,email=email)
        new_user.set_password(password)
        new_user.save()
        return validated_data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ('user',)

class UserUpdateSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(required=False)
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name','userprofile')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile')

        # Update User data
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        
        # Update UserProfile data
        instance.userprofile.age = profile_data.get('age', instance.userprofile.age)
        instance.userprofile.gender = profile_data.get('gender', instance.userprofile.gender)
        instance.userprofile.area = profile_data.get('area', instance.userprofile.area)

        instance.save()

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class TableSerializer(serializers.ModelSerializer):
    host = UserSerializer()
    game = GameSerializer()
    class Meta:
        model = Table
        fields =  fields = ['id','host','game','player_number','game_date','start_time','game_status' ,'game_location','activePlayers']

class TableUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['game','player_number','game_date','start_time','game_location']

class CloseTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['game_status',]

class PlayerSerializer(serializers.ModelSerializer):
    table = TableSerializer()
    player = UserSerializer()
    class Meta:
        model = Player
        fields = '__all__'

class ActivatePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['status',]


