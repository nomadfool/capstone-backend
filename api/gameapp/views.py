from django.shortcuts import render
from rest_framework.generics import ListAPIView,RetrieveAPIView,RetrieveUpdateAPIView,DestroyAPIView,CreateAPIView

from .serializers import (UserCreateSerializer,
                          UserUpdateSerializer,
                          GameSerializer,
                          TableSerializer,
                          TableUpdateSerializer,
                          PlayerSerializer,
                          ActivatePlayerSerializer,
                          CloseTableSerializer,)

from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from gameapp.models import UserProfile,Game,Table,Player

from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
import json
from django.core import serializers
from django.http import Http404
from rest_framework import status


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer


class UpdateProfile(APIView):

    def put(self, request):
        try:
            get_query = User.objects.get(id = request.user.id)
            serializer = UserUpdateSerializer(get_query, data=request.data)
        except User.DoesNotExist:
            return  Response()  
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

class PlayerCreateAPIView(CreateAPIView):
    serializer_class = PlayerSerializer

    def perform_create(self, serializer):
        serializer.save(player=self.request.user)

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

