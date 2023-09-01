from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


def get_upload_path(instance, filename):
    return f"post_pics/{instance.user.username}/{filename}"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_pics', blank=True, null=True)
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
        

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    def __str__(self) -> str:
        return f"Comment by {self.author.username} on {self.post.caption}"
    
    def is_liked_by(self,user):
        return self.likes.filter(pk=user).exists()
    
    def toggle_like(self,user):
        if user in self.likes.all():
            self.likes.remove(user)
            return False
        
        else:
            self.likes.add(user)
            return True
        
class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    parent_reply = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='liked_replies', blank=True)

    def __str__(self) -> str:
        return f"Reply by {self.author.username} on {self.comment.text}"
    
    def is_liked_by(self,user):
        return self.likes.filter(pk=user).exists()
    
    def toggle_like(self,user):
        if user in self.likes.all():
            self.likes.remove(user)
            return False
        
        else:
            self.likes.add(user)
            return True