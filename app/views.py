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

def filter_recipes(request):
    context = {}

    recipe_prepping_time_in_minutes = get_recipe_time_minutes(request)
    recipe_authors = get_recipe_authors(request)
    recipe_temperature = get_cooking_temp(request)

    
    if request.method == "POST":
        all_data = []

        prep_time_in_minutes = request.POST.get('prep_time_in_minutes')
        recipe_author = request.POST.get('recipe_author')
        recipe_temp = request.POST.get('cooking_temp')

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
                    
                    

                


                    print(f"This is the objects {i} {i.cooking_temp}")
                context['tempcheck'] = temp
            

                
                
            print(f"MinTemp:  {mintemp}")
            print(f"MaxTemp: {maxtemp}")

        if recipe_author:
            all_recipes = RecipeData.objects.filter(recipe_author=recipe_author)
            all_data.extend(all_recipes)

        if prep_time_in_minutes:
            all_recipes = RecipeData.objects.filter(prep_time_in_minutes=prep_time_in_minutes)
            all_data.extend(all_recipes)

        
        filter_type = request.POST.getlist("filterItem")
        if filter_type:
            print("Success")
            for option in filter_type:
                
                all_recipes = RecipeData.objects.filter(recipe_type=option)
                print(all_recipes)
                all_data.extend(all_recipes)

        

        context['result'] = all_data

    
    context['recipe_authors'] = recipe_authors

    context['recipe_prepping_time_in_minutes'] = recipe_prepping_time_in_minutes

    
    context['recipes'] = RecipeData.objects.all()

    return render(request, 'filterrecipes.html', context)

def get_recipe_authors(request):
    
    recipe_authors = RecipeData.objects.values_list('recipe_author', flat=True).distinct()
    

    
    return recipe_authors

def get_recipe_time_minutes(request):
    recipe_prepping_time_in_minutes = RecipeData.objects.values_list('prep_time_in_minutes', flat=True).distinct()

    return recipe_prepping_time_in_minutes
    

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
    return render(request, 'builtinchoices.html')

def forums(request):
    return render(request,'forums.html')

def share(request):
    return render(request, 'sharing.html')

