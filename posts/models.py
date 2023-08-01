from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

def get_upload_path(instance, filename):
    return f"post_pics/{instance.user.username}/{filename}"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    caption = models.TextField()
    no_of_likes = models.IntegerField(default=0)
    date_posted = models.DateTimeField(default=timezone.now)
                                                            
    def is_liked_by(self,user):
        return self.likes.filter(user=user).exists()

    def __str__(self) -> str:
        return self.caption

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)


    def __str__(self) -> str:
        return self.username
    
class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.user