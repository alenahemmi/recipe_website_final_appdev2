"""
URL configuration for recipe_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from recipe_app.views import home, AccountDetail, RecipeList, RecipeDetail, RecipeCreate, AccountCreate, RecipeEdit, AccountEdit, ToggleFavorite
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),  
    path('account/<str:username>/', AccountDetail.as_view(), name='account_detail'), 
    path('account/<str:username>/edit/', AccountEdit.as_view(), name='account_edit'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path("register/", AccountCreate.as_view(), name="account_create"),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('recipe/', RecipeList.as_view(), name='recipe_list'), 
    path('recipe/<int:pk>/', RecipeDetail.as_view(), name='recipe_detail'), 
    path('recipe/<int:pk>/edit/', RecipeEdit.as_view(), name='recipe_edit'),
    path('recipe/new/', RecipeCreate.as_view(), name='recipe_create'),
    path('recipe/favorite/<int:pk>/', ToggleFavorite.as_view(), name='toggle_favorite'),
]
