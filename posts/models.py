from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    id         = models.AutoField(primary_key = True)
    content    = models.TextField()
    updated_on = models.DateTimeField(auto_now = True)
    created_on = models.DateTimeField(auto_now_add = True)
    user       = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "posts")
    likes      = models.ManyToManyField(User, related_name = "likes", blank = True)
    
    class Meta:
        db_table = 'posts'
        ordering = ['-created_on']

    def add_like(self, liker):
        self.likes.add(liker)
        self.save()

    def remove_like(self, unliker):
        self.likes.remove(unliker)
        self.save()
