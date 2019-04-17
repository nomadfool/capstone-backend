from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,default = 1)
	age =  models.IntegerField(blank=True, null=True)
	gender = models.CharField(max_length=1,blank=True, null=True)
	area = models.CharField(max_length=100,blank=True, null=True)


class Connection(models.Model):
	player = models.ForeignKey(UserProfile, related_name = "main_player",on_delete=models.CASCADE,default = 1)
	friend = models.ForeignKey(UserProfile, related_name = "player_friend",on_delete=models.CASCADE,default = 1)
	status = models.BooleanField(default=True)

class Game(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	min_player = models.IntegerField(default=2)
	max_player = models.IntegerField(default=2)
	play_time = models.DecimalField(max_digits=5, decimal_places=2)

class Table(models.Model):
	host = models.ForeignKey(User, on_delete=models.CASCADE,default = 1)
	game = models.ForeignKey(Game, on_delete=models.CASCADE,default = 1)
	player_number = models.IntegerField(default=1)
	game_date  = models.DateField()
	start_time = models.TimeField()
	game_status = models.BooleanField(default=True)
	game_location = models.CharField(max_length=100)

	def activePlayers(self):
		 playerCount = self.player_set.filter(status = True).count()
		 return playerCount

class Player(models.Model):
	table = models.ForeignKey(Table, on_delete=models.CASCADE,default = 1)
	player = models.ForeignKey(User, on_delete=models.CASCADE,default = 1)
	play_as =  models.CharField(max_length=50,default = 'Player')
	status = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_profile(sender,instance,**kwargs):
	if kwargs.get('created', False):
		UserProfile.objects.create(user=instance)

@receiver(post_save, sender=Table)
def createHost(sender,instance,**kwargs):
	if kwargs.get('created', False):
		Player.objects.create(table=instance,player =instance.host,play_as = 'Host',status = 1)

@receiver(post_save, sender=Player)
def notifyHost(sender,instance,**kwargs):
	if kwargs.get('created', False):
		try:
			hoster = Player.objects.get(table=instance.table,play_as='Host')
		except Player.DoesNotExist:
			return
		if(hoster.player != instance.player):
			send_mail('New Player',
					  instance.player.first_name +' '+instance.player.last_name + 'like to join the '+ instance.table.game.name,
					  'Notification@gamemember.com',
					  [instance.player.email],
					  fail_silently=False,)
	elif (instance.status):
		send_mail('Activated',
					instance.player.first_name +' '+instance.player.last_name + 'you are welcome  join the '+ instance.table.game.name,
					'Notification@gamemember.com',
					[instance.player.email],
					fail_silently=False,)



