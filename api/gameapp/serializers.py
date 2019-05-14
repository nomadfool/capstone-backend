from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile,Game,Table,Player,Connection




class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['age','gender','image','area']

class UserSerializer(serializers.ModelSerializer):
    userprofile =  UserProfileSerializer()
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email','userprofile']

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


class UserUpdateSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name','userprofile')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile')
        print(validated_data)
        # Update User data
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        
        # Update UserProfile data
        
        profile =instance.userprofile
        profile.age = profile_data.get('age', instance.userprofile.gender)
        profile.gender = profile_data.get('gender', instance.userprofile.gender)
        profile.area = profile_data.get('area', instance.userprofile.area)
        profile.image = profile_data.get('image', instance.userprofile.image)

        profile.save()
        # instance.userprofile.age = profile_data['age']
        # instance.userprofile.gender = profile_data.get('gender', instance.userprofile.gender)
        # # instance.userprofile.image = profile_data.get('image', instance.userprofile.image)
        # instance.userprofile.area = profile_data.get('area', instance.userprofile.area)
        # instance.userprofile.save()
        instance.save()
        return instance

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class TableSerializer(serializers.ModelSerializer):
    host = UserSerializer()
    game = GameSerializer()
    class Meta:
        model = Table
        fields =  fields = ['id','name','description','host','game','player_number','game_date','start_time','game_status' ,'game_location','activePlayers']

class TableUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['name','description','game','player_number','game_date','start_time','game_location']

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

class PlayerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

        def create(self, validated_data):
            # table = validated_data['table']
            # player = validated_data['player']
            # play_as = validated_data['play_as']
            # status = validated_data['status']
            # new_player = Player.objects.create(table=table,player=player,play_as=play_as,status=status)
            # return new_player
            return Player.objects.create(**validated_data)

class ActivatePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['status',]

class ConnectionSerializer(serializers.ModelSerializer):
    player = UserSerializer()
    friend = UserSerializer()
    class Meta:
        model = Connection
        fields = ['id','player','friend','status']










