from django.db import models
from django.contrib.auth.models import User

class Film(models.Model):
    title = models.CharField(max_length=100 , verbose_name = "name")
    director = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    poster = models.ImageField(upload_to='worstFilms/images', blank= True, null= True)
    release_year = models.IntegerField(blank = True , null = True)
    review = models.TextField(default = '')
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    class rate_choices(models.IntegerChoices):
        one = -1,
        two = -2, 
        three = -3,
        four = -4,
        five = -5,

    rate = models.IntegerField(choices = rate_choices.choices)

    def count_likes(self):
        return self.plike.count()

    def user_can_like(self, user):
        user_like = user.ulikes.all()
        qs = user_like.filter(post=self)
        if qs.exists():
            return True
        return False

    
    def __str__(self):
        return self.title

    """def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})"""

class Comment(models.Model):
    user= models.ForeignKey(User, on_delete=models.PROTECT , related_name = 'ucomment')
    body= models.TextField()
    film= models.ForeignKey(Film, on_delete=models.CASCADE, related_name= 'fcomment')
    reply = models.ForeignKey("self", on_delete=models.CASCADE, blank = True, null= True, related_name= 'rcomment')
    is_reply= models.BooleanField(default= False)
    pub_date= models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering= ['-pub_date']

    def __str__(self):
        return f'{self.user}-{self.body[:30]}'

class Like(models.Model):
    post = models.ForeignKey(Film, on_delete=models.CASCADE, related_name= 'plike')
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='ulikes')

    def __str__(self):
        return f'{self.user} liked {self.post}'
    







