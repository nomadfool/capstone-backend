# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from gameapp.models import  UserProfile,Table,Player
# from django.contrib.auth.models import User
# from django.core.mail import send_mail

# # @receiver(post_save, sender=User)
# def create_profile(sender,instance,**kwargs):
# 	print(kwargs)
# 	if kwargs.get('created', False):
# 		UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=Table)
# def createHost(sender,instance,**kwargs):
# 	if kwargs.get('created', False):
# 		Player.objects.create(table=instance,player =instance.host,play_as = 'Host',status = 1)

# @receiver(post_save, sender=Player)
# def notifyHost(sender,instance,**kwargs):
# 	if kwargs.get('created', False):
# 		try:
# 			hoster = Player.objects.get(table=instance.table,play_as='Host')
# 		except Player.DoesNotExist:
# 			return
# 		if(hoster.player != instance.player):
# 			send_mail('New Player',
# 					  instance.player.first_name +' '+instance.player.last_name + 'would like to join the '+ instance.table.game.name,
# 					  'Notification@gamemember.com',
# 					  [instance.player.email],
# 					  fail_silently=False,)



# @receiver(post_save, sender=Table)
# def createHost(sender, **kwargs):
# 	btrans = transaction.savepoint()
# 	try:
# 		with transaction.atomic():
# 			if kwargs.get('created', False):
# 				Player.objects.get_or_create(table=kwargs.get('instance'),player = instanse.host,play_as = 'Host',status = 1)
# 	except Exception:
# 		transaction.savepoint_rollback(btrans)
