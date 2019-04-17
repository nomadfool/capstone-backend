
from django.contrib import admin
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from gameapp.views import (UserCreateAPIView,
						   UpdateProfile,
						   GameListView,
						   GameDetailsAPIView,
						   GameCreateAPIView,
						   GameUpdateAPIView,
						   GameDeleteAPIView,
						   TableListView,
						   TableDetailsAPIView,
						   TableCreateAPIView,
						   TableUpdateAPIView,
						   TableDeleteAPIView,
						   CloseTableAPIView,
						   PlayerListView,
						   PlayerDetailsAPIView,
						   PlayerCreateAPIView,
						   PlayerDeleteAPIView,
						   ActivatePlayerAPIView,

						   )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', obtain_jwt_token, name='login'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('profile/update/', UpdateProfile.as_view(), name='profile_update'),
    path('game/list/', GameListView.as_view(), name='game_list'),
    path('game/details/<int:game_id>', GameDetailsAPIView.as_view(), name='game_details'),
    path('game/add/', GameCreateAPIView.as_view(), name='game_add'),
    path('game/update/<int:game_id>', GameUpdateAPIView.as_view(), name='game_update'),
    path('game/delete/<int:game_id>', GameDeleteAPIView.as_view(), name='game_delete'),
    path('table/list/', TableListView.as_view(), name='taleb_list'),
    path('table/details/<int:table_id>', TableDetailsAPIView.as_view(), name='table_details'),
    path('table/add/', TableCreateAPIView.as_view(), name='table_add'),
    path('table/update/<int:table_id>', TableUpdateAPIView.as_view(), name='table_update'),
    path('table/delete/<int:table_id>', TableDeleteAPIView.as_view(), name='table_delete'),
    path('table/close/<int:table_id>', CloseTableAPIView.as_view(), name='table_close'),
    path('player/list/', PlayerListView.as_view(), name='player_list'),
    path('player/details/<int:player_id>', PlayerDetailsAPIView.as_view(), name='player_details'),
    path('player/add/', PlayerCreateAPIView.as_view(), name='player_add'),
    path('player/activate/<int:player_id>', ActivatePlayerAPIView.as_view(), name='player_active'),
    path('player/delete/<int:player_id>', PlayerDeleteAPIView.as_view(), name='player_delete'), 
]