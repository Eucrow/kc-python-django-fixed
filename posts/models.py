from django.db import models
from django.contrib.auth.models import User

from categories.models import Category
from posts.validators import badwords


class Post(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=150, validators=[badwords])
    introduction = models.TextField(max_length=150, validators=[badwords])
    content = models.TextField(max_length=15000, validators=[badwords])
    url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    publication_date = models.DateField()
    publication_time = models.TimeField()
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title
