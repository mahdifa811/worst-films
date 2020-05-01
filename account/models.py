from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from worstFilms.models import Film

class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def add_profile(sender, **kwargs):
    if kwargs['created']:
        p = Profile(user= kwargs['instance'])
        p.save()

class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'follower')
    to_user= models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'following')
    created_date= models.DateTimeField(auto_now_add= True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f'{self.from_user} is following  {self.to_user}'
    


