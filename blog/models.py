from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=150)
    desc = models.TextField()
    author = models.CharField(max_length=50)
    views = models.IntegerField(default=0)
    date_added=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)


# sno
# comment
# User
# Post
# pareent
# timestamp
class BlogComment(models.Model):
    sno= models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    time_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[0:10] + "...  by  " + self.user.username


