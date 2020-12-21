from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=150)
    desc = models.TextField()
    author = models.CharField(max_length=50)
    date_added=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)
