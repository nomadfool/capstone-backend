from django.contrib import admin
from gameapp.models import UserProfile,Game,Table,Player,Connection

admin.site.register(UserProfile)
admin.site.register(Game)
admin.site.register(Table)
admin.site.register(Player)
admin.site.register(Connection)

