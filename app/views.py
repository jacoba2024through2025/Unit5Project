from django.http.response import HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import render
from typing import Dict
from dataclasses import dataclass

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


def filter_recipes(request):
    return render(request, 'filterrecipes.html')

def built_in_choices(request):
    return render(request, 'builtinchoices.html')

def forums(request):
    return render(request,'forums.html')

def share(request):
    return render(request, 'sharing.html')

