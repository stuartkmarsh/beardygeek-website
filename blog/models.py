from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

POST_STATUS = (
               ('P', 'Published'),
               ('U', 'Unpublished'),
)

class Tag(models.Model):
    text = models.CharField(max_length=75)
    slug = models.CharField(max_length=75)
    
    def __unicode__(self):
        return self.text
    
class Category(models.Model):
    text = models.CharField(max_length=75)
    slug = models.CharField(max_length=75)
    
    def __unicode__(self):
        return self.text
    
    class Meta:
        verbose_name_plural = "categories"

class Post(models.Model):
    title = models.CharField(max_length=75)
    slug = models.CharField(max_length=75)
    content = models.TextField()
    author = models.ForeignKey(User, unique=True)
    post_date = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=1, choices=POST_STATUS)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    
    def __unicode__(self):
        return self.title
    