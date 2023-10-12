from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')
    bio = models.TextField(blank=True)
    #if the user does not provide, the email, its still okay
    email = models.EmailField(blank=True)
    def __str__(self) -> str:
        return f"{self.user.username} profile"


    def save(self, *args, **kwargs): 
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)