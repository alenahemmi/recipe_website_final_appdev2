from django.shortcuts import render, get_object_or_404
from django.views import View
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Account, Recipe, Hashtag, Comment
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse


# Create your views here.
def home(request):
    return render(request, "recipe_app/home.html")


# ACCOUNT TINGS ********************************************************************

class AccountDetail(DetailView):
    model = Account
    template_name = 'recipe_app/account_detail.html'
    context_object_name = 'account'
    
    def get_object(self):
        username = self.kwargs.get('username')
        return get_object_or_404(Account, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorites'] = self.object.favorites.all()
        context['created_recipes'] = self.object.recipe_set.all()
        return context



class AccountCreate(View):
    template_name = "recipe_app/account_create.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        bio = request.POST.get("bio")

        if not (username and first_name and last_name and password):
            return render(request, self.template_name, {"error": "All fields are required."})

        if Account.objects.filter(username=username).exists():
            return render(request, self.template_name, {"error": "Username already taken."})
        
        
        user = Account.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=make_password(password),
            bio=bio
        )

        login(request, user)
        return redirect("account_detail", username=user.username)




class AccountEdit(LoginRequiredMixin, View):
    def get(self, request, username):
        if request.user.username != username:
            return redirect('account_detail', username=request.user.username)

        account = Account.objects.get(username=username)
        return render(request, 'recipe_app/account_edit.html', {'account': account})


    def post(self, request, username):
        if request.user.username != username:
            return redirect('account_detail', username=request.user.username)
        account = Account.objects.get(username=username)

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        bio = request.POST.get('bio')

        account.first_name = first_name
        account.last_name = last_name
        account.bio = bio
        account.save()

        return redirect('account_detail', username=account.username)



# RECIPE STUFF ********************************************************************


class RecipeList(ListView):
    model = Recipe
    template_name = 'recipe_list.html'
    context_object_name = 'recipes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q:
            context['recipes'] = Recipe.objects.filter(recipe_name__icontains=q)
        return context


class RecipeDetail(DetailView):
    model = Recipe
    template_name = 'recipe_app/recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(recipe=self.object)

        if self.request.user == self.object.creator:
            context['can_edit'] = True
        else:
            context['can_edit'] = False

        return context

    def post(self, request, *args, **kwargs):
        recipe = self.get_object()
        if request.user.is_authenticated:
            content = request.POST.get('content')
            if content:
                Comment.objects.create(
                    content=content,
                    user=request.user,
                    recipe=recipe
                )

        if 'delete_comment_id' in request.POST:
            comment_id = request.POST.get('delete_comment_id')
            comment = Comment.objects.get(id=comment_id)

            if comment.user == request.user:
                comment.delete()

        return redirect('recipe_detail', pk=recipe.pk)




class RecipeCreate(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'recipe_app/recipe_create.html')

    def post(self, request):
        recipe_name = request.POST.get('recipe_name')
        ingredients = request.POST.get('ingredients')
        directions = request.POST.get('directions')
        hashtags_input = request.POST.get('hashtags')

        recipe = Recipe.objects.create(
            recipe_name=recipe_name,
            ingredients=ingredients,
            directions=directions,
            creator=request.user
        )

        if hashtags_input:
            hashtags_list = hashtags_input.split(',')
            for tag in hashtags_list:
                tag = tag.strip()
                if tag:
                    hashtag, created = Hashtag.objects.get_or_create(hashtag=tag, recipe=recipe)

        return redirect('recipe_detail', pk=recipe.pk)
    



class RecipeEdit(LoginRequiredMixin, View):
    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        
        if recipe.creator != request.user:
            return redirect('recipe_detail', pk=recipe.pk)
        
        return render(request, 'recipe_app/recipe_edit.html', {'recipe': recipe})
    
    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        
        if recipe.creator != request.user:
            return redirect('recipe_detail', pk=recipe.pk)
        
        recipe_name = request.POST.get('recipe_name')
        ingredients = request.POST.get('ingredients')
        directions = request.POST.get('directions')
        hashtags_input = request.POST.get('hashtags', '').strip()  
        

        if recipe_name and ingredients and directions:
            recipe.recipe_name = recipe_name
            recipe.ingredients = ingredients
            recipe.directions = directions
            recipe.save()  

            hashtags_list = [tag.strip() for tag in hashtags_input.split(',') if tag.strip()]
            
            recipe.hashtags.all().delete()

            for hashtag in hashtags_list:
                Hashtag.objects.get_or_create(hashtag=hashtag, recipe=recipe)
            
            return redirect('recipe_detail', pk=recipe.pk)
        
        else:
            return render(request, 'recipe_app/recipe_edit.html', {
                'recipe': recipe,
                'error': 'All fields are required.'
            })
        



class ToggleFavorite(LoginRequiredMixin, View):
    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user

        favorited = False
        if recipe in user.favorites.all():
            user.favorites.remove(recipe)
            favorited = False
        else:
            user.favorites.add(recipe)
            favorited = True

        return JsonResponse({'favorited': favorited})