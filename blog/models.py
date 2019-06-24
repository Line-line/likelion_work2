from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published')
    body = models.TextField()

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:100]
        # 100개까지만 보여주고 그 이상은 detail로 들어가서 보여주게끔

class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete = models.CASCADE, related_name = "comments")
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    body = models.CharField(max_length = 500)
    # 게시글 하나에 댓글 여러개
