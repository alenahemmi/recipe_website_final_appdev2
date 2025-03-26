from django.db import models
from django.contrib.auth.models import AbstractUser

class Account(AbstractUser):
    bio = models.TextField(blank=True)
    favorites = models.ManyToManyField('Recipe', related_name='favorited_by', blank=True)

    def __str__(self):
        return self.username

class Recipe(models.Model):
    recipe_name = models.CharField(max_length=255)
    ingredients = models.TextField(default="Not specified")
    directions = models.TextField(default="Not specified")
    creator = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.recipe_name

class Hashtag(models.Model):
    hashtag = models.CharField(max_length=100)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="hashtags")

    def __str__(self):
        return self.hashtag

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.user} on {self.recipe}"

