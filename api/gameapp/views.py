from django.shortcuts import render
from rest_framework.generics import ListAPIView,RetrieveAPIView,RetrieveUpdateAPIView,DestroyAPIView,CreateAPIView

from .serializers import (UserCreateSerializer,
                          UserUpdateSerializer,
                          GameSerializer,
                          TableSerializer,
                          TableUpdateSerializer,
                          PlayerSerializer,
                          PlayerCreateSerializer,
                          ActivatePlayerSerializer,
                          CloseTableSerializer,
                          ConnectionSerializer,
                          UserSerializer)

from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from gameapp.models import UserProfile,Game,Table,Player,Connection

from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
import json
from django.core import serializers
from django.http import Http404
from rest_framework import status
from django.db.models import Q


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer


class UpdateProfile(APIView):

    def put(self, request):
        try:
            get_query = User.objects.get(id = request.user.id) 
            serializer = UserUpdateSerializer(get_query, data=request.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GameListView(ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['name','description','min_player','max_player','play_time']

class GameDetailsAPIView(RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'game_id'

class GameCreateAPIView(CreateAPIView):
    serializer_class = GameSerializer

class GameUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'game_id'

class GameDeleteAPIView(DestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'game_id'

class TableListView(ListAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ('__all__')

class TableDetailsAPIView(RetrieveAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'table_id'

class TableCreateAPIView(CreateAPIView):
    serializer_class = TableSerializer

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

class TableUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Table.objects.all()
    serializer_class = TableUpdateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'table_id'

class TableDeleteAPIView(DestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = TableSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'table_id'

class CloseTableAPIView(RetrieveUpdateAPIView):
    queryset = Table.objects.all()
    serializer_class = CloseTableSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'table_id'


class PlayerListView(ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ('__all__')

class PlayerDetailsAPIView(RetrieveAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'player_id'

class PlayerCreateAPIView(APIView):

    def checkexisting(self,request,table):
        try:
            player = self.request.user
            joined_before = Player.objects.get(table = table,player = player)
            return False
        except Player.DoesNotExist:
            return True

    def post(self,request,*args, **kwargs):
        if self.checkexisting(request,table=request.data.get('table')):
            serializer = PlayerCreateSerializer(data=request.data)
            if serializer.is_valid():  
                serializer.save(player = self.request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_302_FOUND)
   

class PlayerDeleteAPIView(DestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'player_id'

class ActivatePlayerAPIView(RetrieveUpdateAPIView):
    queryset = Player.objects.all()
    serializer_class = ActivatePlayerSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'player_id'


# class UserConnectionView(APIView):

#     def get(self,request):
#         get_query =  User.objects.filter(~Q(id = request.user.id))
#         serializer = UserSerializer(get_query, many=True,)
#         return Response(serializer.data)



class UserConnectionView(APIView):

    def get(self,request):
        get_query =  User.objects.filter(~Q(id = request.user.id))
        serializer = UserSerializer(get_query, many=True,)
        return Response(serializer.data)

class CtrlFriendAPIView(APIView):

    def get(self,request):
        try:
            if (request.data.get('p_id')):
                get_query = Connection.objects.get(id=p_id)
            else:
                get_query = Connection.objects.filter(player = request.user,status=True)

            serializer = ConnectionSerializer(get_query, many=True,)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)

    
    def post(self,request,*args, **kwargs):
        if(request.data.get('p_id')):
            try:
                user = User.objects.get(pk = p_id)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            try:
                friend= Connection.objects.get(player = request.user,
                friend = user)
                friend.status = True
                friend.save()
            except:
                if Connection.DoesNotExist:
                    try:
                        friend = Connection.objects.create(player = request.user,
                        friend = user,status = True)
                    except:
                        return Response(status.HTTP_304_NOT_MODIFIED) 
                else:
                    return Response(status=status.HTTP_304_NOT_FOUND)

            serializer = ConnectionSerializer(friend, many=False)
            return Response(serializer.data,status=status.HTTP_200_OK)

    def delete(self,request,*args, **kwargs):
        if(request.data.get('p_id')):
            try:
                get_query = Connection.objects.filter(id = p_id)
                get_query.delete()
            except Connection.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_204_NO_CONTENT)


class CtrlBlackAPIView(APIView):

    def get(self,request):
        try:
            if(request.data.get('p_id')):
                get_query = Connection.objects.filter(player = request.user,status=False)
            else:
                get_query = Connection.objects.filter(pk=p_id, player = request.user,status=False)

            serializer = ConnectionSerializer(get_query, many=True,)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)

    
    def post(self,request,*args, **kwargs):
        if(request.data.get('p_id')):
            try:
                user = User.objects.get(pk = p_id)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            try:
                friend= Connection.objects.get(player = request.user,
                friend = user)
                friend.status = False
                friend.save()
            except:
                if Connection.DoesNotExist:
                    try:
                        friend = Connection.objects.create(player = request.user,
                        friend = user,status = False)
                    except:
                        return Response(status.HTTP_304_NOT_MODIFIED) 
                else:
                    return Response(status=status.HTTP_304_NOT_FOUND)

            serializer = ConnectionSerializer(friend, many=False)
            return Response(serializer.data,status=status.HTTP_200_OK)





