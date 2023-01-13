from django.db import models
from posts.models import Post
from django.contrib.auth.models import User

class Comment(models.Model):
    id         = models.AutoField(primary_key = True)
    post       = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "comments")
    user       = models.ForeignKey(User, on_delete = models.CASCADE)
    body       = models.TextField()
    updated_on = models.DateTimeField(auto_now = True)
    created_on = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'comments'
        ordering = ['created_on']
