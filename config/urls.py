"""
URL configuration for config project.

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

from app import views
urlpatterns = [
    path("", views.detail_view, name='home'),
    path("team/<str:recipes_name>/", views.detail_view, name='recipe_detail'),
    path('filterrecipes/', views.filter_recipes, name='filterrecipes'),
    path('builtinchoices/', views.built_in_choices, name='builtinchoices'),
    path('recipecreation/', views.create_recipe_form, name="recipecreation"),
    path('currentrecipe/', views.current_recipe, name="currentrecipe"),
    path('forums/', views.forums, name='forums'),

    path('share',views.share, name='share'),
    
    
   
    path("admin/", admin.site.urls),
    
]
