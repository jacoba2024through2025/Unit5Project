from django.http.response import HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import render
from typing import Dict
from dataclasses import dataclass
from app.models import RecipeData

@dataclass
class Recipes:
    recipe_name: str
    
    #ingredients: str
    instructions: str
    #servings: int
    #prepping_time: int
    #serving_time: int
    #user_name: str
    



recipedata: Dict[str, Recipes] = {
    "recipe1": Recipes(
        recipe_name="Classic Grilled Cheese",
        instructions="""
            1. Lay out the bread slices. Place two slices of cheese between two slices of bread to make each sandwich.
            2. Spread butter on the outer sides of each sandwich, ensuring to cover the whole surface.
            3. Heat a non-stick skillet over medium heat. Place the sandwiches butter-side down in the skillet. Cook until golden brown, about 3-4 minutes. Butter the top side of the sandwich, then flip it over and cook until the second side is golden brown and the cheese is melted.
            4. Remove the sandwiches from the skillet, let them cool for a minute, then cut diagonally. Serve warm.

        """,
        
    ),
    "recipe2": Recipes(
        recipe_name="Tomato Basil Pasta",
        instructions="""
        1. Cook Spaghetti according to package instructions. Drain, reserving 1 cup of the pasta water.
        2. In a skillet, heat olive oil, Saute garlic until fragrant, then add tomatoes, salt, and pepper. Cook until sauce thickens.
        3. Add the cooked spaghetti to the skillet, tossing to combine, and adding reserved pasta water if needed.
        4. Off the heat, garnish with basil and Parmasean. Serve immediately.
        
        
        """,
        
    ),
    
}


def detail_view(request: HttpRequest, recipes_name: str=None) -> HttpResponse:
    if recipes_name:
        recipe = recipedata.get(recipes_name)
        
        return render(request, "recipes.html", {'recipe': recipe})
    
    
    return render(request, "recipes.html", {'recipes': recipedata.keys()})


from django.shortcuts import render
from .models import RecipeData
from app.forms import NewRecipeCreation

def filter_recipes(request):
    context = {}

    recipe_prepping_time_in_minutes = get_recipe_time_minutes(request)
    recipe_prepping_time_in_hours = get_recipe_time_hours(request)
    recipe_authors = get_recipe_authors(request)
    

    
    if request.method == "POST":
        all_data = []

        prep_time_in_minutes = request.POST.get('prep_time_in_minutes')
        prep_time_in_hours = request.POST.get('prep_time_in_hours')
        recipe_author = request.POST.get('recipe_author')
        

        #mintemp = request.POST.getlist("min_temp")
        #maxtemp = request.POST.getlist("max_temp")

        
        mintemp = request.POST.get("min_temp")
        maxtemp = request.POST.get("max_temp")
        if mintemp != None and maxtemp!=None:

            mintemp = int(mintemp)
            maxtemp = int(maxtemp)

        

            temp = []

            for i in RecipeData.objects.iterator():
                
                if i.cooking_temp != None and i.cooking_temp >= mintemp and i.cooking_temp <= maxtemp:
                    temp.append(i)
                    
                    

                


                    
                context['tempcheck'] = temp
            

                
                
            print(f"MinTemp:  {mintemp}")
            print(f"MaxTemp: {maxtemp}")

        if recipe_author:
            all_recipes = RecipeData.objects.filter(recipe_author=recipe_author)
            all_data.extend(all_recipes)

        if prep_time_in_minutes:
            all_recipes = RecipeData.objects.filter(prep_time_in_minutes=prep_time_in_minutes)
            all_data.extend(all_recipes)
        
        if prep_time_in_hours:
            all_recipes = RecipeData.objects.filter(prep_time_in_hours=prep_time_in_hours)
            all_data.extend(all_recipes)

        
        filter_type = request.POST.getlist("filterItem")
        if filter_type:
            
            for option in filter_type:
                
                all_recipes = RecipeData.objects.filter(recipe_type=option)
                
                all_data.extend(all_recipes)

        

        context['result'] = all_data

    
    context['recipe_authors'] = recipe_authors

    context['recipe_prepping_time_in_minutes'] = recipe_prepping_time_in_minutes

    context['recipe_prepping_time_in_hours'] = recipe_prepping_time_in_hours
    
    

    
    context['recipes'] = RecipeData.objects.all()



    return render(request, 'filterrecipes.html', context)




def get_recipe_authors(request):
    
    recipe_authors = RecipeData.objects.values_list('recipe_author', flat=True).distinct()
    

    
    return recipe_authors

def get_recipe_time_minutes(request):
    recipe_prepping_time_in_minutes = RecipeData.objects.values_list('prep_time_in_minutes', flat=True).distinct()

    return recipe_prepping_time_in_minutes

def get_recipe_time_hours(request):
    recipe_prepping_times_in_hours = RecipeData.objects.values_list('prep_time_in_hours', flat=True).distinct()
    return recipe_prepping_times_in_hours
    

def get_cooking_temp(request):
    recipe_cooking_temp = RecipeData.objects.values_list('cooking_temp', flat=True).distinct()

    return recipe_cooking_temp

def recipe_view(request):
    
    recipe_authors = RecipeData.objects.values_list('recipe_author', flat=True).distinct()
    
    selected_author = None
    
    if request.method == 'POST':
        selected_author = request.POST.get('recipe_author')
    
    return render(request, 'filterrecipes.html', {
        'recipe_authors': recipe_authors,
        'selected_author': selected_author
    })

















def built_in_choices(request):
    context = {}

    all_data = []

    filter_type = request.POST.get("search_bar")
    if filter_type:
        context['usersearchname'] = filter_type
        
        all_data = RecipeData.objects.none()

        
        for option in filter_type.split():
            all_data = all_data | RecipeData.objects.filter(ingredients_needed__icontains=option)
        if not all_data:
            context['userwrongname'] = filter_type

    context['result'] = all_data



        
            
        
    
    print(f"All Data: {all_data}")
    context['result'] = all_data

    
    return render(request, 'builtinchoices.html', context)

def forums(request, recipe_author):
    if request.method == 'POST':
        selected_author = request.POST.get('recipe_author')
        rating = request.POST.get('rating')
        feedback = request.POST.get('feedback')

        if selected_author and rating:
            try:
                
                rating = int(rating)

                
                recipe = SavedRecipe.objects.filter(recipe_author=selected_author).first()

                if recipe:
                    
                    recipe.rating = rating
                    if feedback:  
                        recipe.feedback = feedback
                    recipe.save()

                    
                    return render(request, 'forums.html', {
                        'recipe_authors': SavedRecipe.objects.values_list('recipe_author', flat=True).distinct(),
                        'selected_author': selected_author,
                        'recipe': recipe,  
                    })

                return HttpResponse("Recipe not found.", status=404)

            except ValueError:
                return HttpResponse("Invalid rating value.", status=400)

    
    selected_author = request.GET.get('recipe_author', '')
    recipe_authors = SavedRecipe.objects.values_list('recipe_author', flat=True).distinct()
    
    
    recipe = None
    recipe = SavedRecipe.objects.filter(recipe_author=recipe_author).first()

    return render(request, 'forums.html', {
        'recipe_authors': recipe_authors,
        'selected_author': selected_author,
        'recipe': recipe,  
    })

def share(request):
    return render(request, 'sharing.html')

def create_recipe(request):
    return render(request,"recipecreation.html")


from .models import SavedRecipe

from django.shortcuts import render, redirect, get_object_or_404
from .models import SavedRecipe

def current_recipe(request):
    
    saved_recipes = SavedRecipe.objects.all()

    if request.method == "POST":
        
        recipe_id_to_delete = request.POST.get('delete_recipe_id')
        if recipe_id_to_delete:
            
            recipe_to_delete = get_object_or_404(SavedRecipe, id=recipe_id_to_delete)
            recipe_to_delete.delete()

            
            return redirect('currentrecipe')  

        
        recipe_name = request.POST.get('recipe_name')
        recipe_author = request.POST.get('recipe_author')
        recipe_type = request.POST.get('recipe_type')
        ingredients_needed = request.POST.get('ingredients_needed')
        recipe_instructions = request.POST.get('recipe_instructions')

        
        cooking_temp = request.POST.get('cooking_temp')
        if cooking_temp == '' or cooking_temp is None:
            cooking_temp = None
        else:
            try:
                cooking_temp = int(cooking_temp)
            except ValueError:
                cooking_temp = None

        prep_time_in_minutes = request.POST.get('prep_time_in_minutes')
        if prep_time_in_minutes == '' or prep_time_in_minutes is None:
            prep_time_in_minutes = None
        else:
            try:
                prep_time_in_minutes = int(prep_time_in_minutes)
            except ValueError:
                prep_time_in_minutes = None

        prep_time_in_hours = request.POST.get('prep_time_in_hours')
        if prep_time_in_hours == '' or prep_time_in_hours is None:
            prep_time_in_hours = None
        else:
            try:
                prep_time_in_hours = int(prep_time_in_hours)
            except ValueError:
                prep_time_in_hours = None

        servings = request.POST.get('servings')
        if servings == '' or servings is None:
            servings = None
        else:
            try:
                servings = int(servings)
            except ValueError:
                servings = None

        
        saved_recipe = SavedRecipe(
            recipe_name=recipe_name,
            recipe_author=recipe_author,
            recipe_type=recipe_type,
            ingredients_needed=ingredients_needed,
            recipe_instructions=recipe_instructions,
            cooking_temp=cooking_temp,
            prep_time_in_minutes=prep_time_in_minutes,
            prep_time_in_hours=prep_time_in_hours,
            servings=servings,
        )
        saved_recipe.save()

        
        saved_recipes = SavedRecipe.objects.all()

    return render(request, "currentrecipe.html", {'saved_recipes': saved_recipes})








from django.shortcuts import render
from .forms import NewRecipeCreation
from .models import RecipeData

from django.shortcuts import render, redirect
from django.contrib import messages  
from .forms import NewRecipeCreation
from .models import RecipeData

def create_recipe_form(request):
    if request.method == 'POST':
        form = NewRecipeCreation(request.POST)
        if form.is_valid():
            
            recipe_author = form.cleaned_data["recipe_author"]
            recipe_name = form.cleaned_data["recipe_name"]
            recipe_type = form.cleaned_data["recipe_type"]
            ingredients_needed = form.cleaned_data["ingredients_needed"]
            recipe_instructions = form.cleaned_data["recipe_instructions"]
            prep_time_in_minutes = form.cleaned_data.get("prep_time_in_minutes")
            prep_time_in_hours = form.cleaned_data.get("prep_time_in_hours")
            cooking_temp_in_fahrenheit = form.cleaned_data.get("Cooking_Temperature_In_Fahrenheit")
            servings = form.cleaned_data.get("servings")

            
            new_recipe = RecipeData(
                recipe_author=recipe_author,
                recipe_name=recipe_name,
                recipe_type=recipe_type,
                ingredients_needed=ingredients_needed,
                recipe_instructions=recipe_instructions,
                prep_time_in_minutes=prep_time_in_minutes,
                prep_time_in_hours=prep_time_in_hours,
                cooking_temp=cooking_temp_in_fahrenheit,
                servings=servings
            )

            new_recipe.save()

            
            messages.success(request, 'Recipe Submitted Successfully!')

            
            return redirect('recipecreation')  

    else:
        form = NewRecipeCreation()

    return render(request, "recipecreation.html", {"form": form})


