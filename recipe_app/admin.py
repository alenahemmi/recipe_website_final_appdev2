from django.contrib import admin
from .models import Account, Recipe, Ingredient, Hashtag, Comment

admin.site.register(Account)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Hashtag)
admin.site.register(Comment)

