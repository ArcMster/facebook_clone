from django.db import models
from django.contrib.auth.models import User
from django_mysql.models import ListCharField
from django.db.models import CharField
# Create your models here.

#sreenath
#fbapp@123

class Post(models.Model):
    image = models.ImageField(upload_to = 'media', blank = True)
    caption = models.CharField(max_length=255)
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    
    likedby = ListCharField(
        base_field = CharField(max_length = 10),
        size = 10,
        max_length = (10*11),
        null = True,
        default = 'no likes'
        
    )

    def __str__(self):
        return str(self.id)

class Liked(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    postid = models.TextField(max_length=10)
    comment = models.TextField(max_length=255)


class Messages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.TextField(max_length=100)
    message = models.TextField(max_length=255)
    
    
    

    

