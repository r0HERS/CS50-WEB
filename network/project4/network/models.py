from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="post_user")
    text = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"Post:{self.id} made by {self.user.username}" 
    
class Follow(models.Model):
    following_user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="folowing_user")
    followed_user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="folowed_user")

    def __str__(self):
        return f"{self.following_user} is following {self.followed_user}" 

class Like(models.Model):
    post = models.ForeignKey("Post",on_delete=models.CASCADE, related_name="liked_post")
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_like")

    def __str__(self):
        return f"{self.user.username} liked {self.post}"  
       