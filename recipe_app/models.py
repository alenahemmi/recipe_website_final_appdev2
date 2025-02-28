from django.db import models

class Account(models.Model):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    favorites = models.ManyToManyField('Recipe', related_name='favorited_by', blank=True)

    def __str__(self):
        return self.username

class Recipe(models.Model):
    recipe_name = models.CharField(max_length=255)
    directions = models.TextField()
    creator = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.recipe_name

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.CharField(max_length=255)
    amount = models.CharField(max_length=100)  # Consider using DecimalField if numeric

    def __str__(self):
        return f"{self.amount} of {self.ingredient}"

class Hashtag(models.Model):
    hashtag = models.CharField(max_length=100)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.hashtag

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.user} on {self.recipe}"
