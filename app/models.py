from django.db import models
from django.core.exceptions import ObjectDoesNotExist



class RecipeData(models.Model):
    recipe_author = models.CharField(max_length=75)
    recipe_name = models.CharField(max_length=75)
    recipe_type = models.CharField(max_length=15, blank= True, null=True)
    ingredients_needed = models.CharField(max_length=600)
    recipe_instructions = models.CharField(max_length=1200)
    prep_time_in_minutes = models.IntegerField(null=True, blank=True)
    prep_time_in_hours = models.IntegerField(null=True, blank=True)
    cooking_temp = models.IntegerField(null=True, blank=True)
    servings = models.IntegerField(null=True, blank= True)

    def __str__(self) -> str:
        return f"{self.recipe_name} by {self.recipe_author}"
    

def add_recipe_in(recipe_author, recipe_name, recipe_type, ingredients_needed, recipe_instructions, prep_time_in_minutes, cooking_temp, servings, prep_time_in_hours):
    stored_recipe = RecipeData.objects.create(recipe_author=recipe_author, recipe_name=recipe_name, recipe_type=recipe_type, ingredients_needed=ingredients_needed, recipe_instructions=recipe_instructions, prep_time_in_minutes=prep_time_in_minutes, prep_time_in_hours=prep_time_in_hours, cooking_temp=cooking_temp, servings=servings)
    return stored_recipe
    

def view_all_recipes():
    return RecipeData.objects.all()

#start of filtering

#filter by recipe name
def filter_recipes_name(recipe_name):
    if recipe_name != None:
        return RecipeData.objects.filter(recipe_name=recipe_name)
    return RecipeData.objects.all()

#filter by recipe author
def filter_recipes_author(recipe_author):
    if recipe_author != None:
        return RecipeData.objects.filter(recipe_author=recipe_author)
    return RecipeData.objects.all()

#filter by recipe type
def filter_recipes_type(recipe_type):
    if recipe_type != None:
        return RecipeData.objects.filter(recipe_type=recipe_type)
    return RecipeData.objects.all()

#filter by ingredients
def filter_recipes_ingredients(ingredients_needed):
    if ingredients_needed != None:
        return RecipeData.objects.filter(ingredients_needed=ingredients_needed)
    return RecipeData.objects.all()

#filter by recipe instructions
def filter_recipes_instructions(recipe_instructions):
    if recipe_instructions != None:
        return RecipeData.objects.filter(recipe_instructions=recipe_instructions)
    return RecipeData.objects.all()

#filter by recipe prep time minutes
def filter_recipes_preptime_minutes(prep_time_in_minutes):
    if prep_time_in_minutes != None:
        return RecipeData.objects.filter(prep_time_in_minutes=prep_time_in_minutes)
    return RecipeData.objects.all()

#filter by recipe prep time hours
def filter_recipes_preptime_hours(prep_time_in_hours):
    if prep_time_in_hours != None:
        return RecipeData.objects.filter(prep_time_in_hours=prep_time_in_hours)
    return RecipeData.objects.all()

#filter by recipe temperature
def filter_recipes_bytemp(cooking_temp):
    if cooking_temp != None:
        return RecipeData.objects.filter(cooking_temp=cooking_temp)
    return RecipeData.objects.all()

#filter by recipe servings
def filter_recipes_byservings(servings):
    if servings != None:
        return RecipeData.objects.filter(servings=servings)
    return RecipeData.objects.all()

#end of filtering

def view_recipe_by_id(recipeid):
    try:
        return RecipeData.objects.get(id=recipeid)
    except ObjectDoesNotExist:
        return None

def update_recipes(recipeid, recipe_name=None, recipe_author=None, recipe_type=None, ingredients_needed=None, recipe_instructions=None, prep_time_in_hours=None, cooking_temp=None, servings=None, prep_time_in_minutes=None):
    try:
        recipe = RecipeData.objects.get(id=recipeid)
        if recipe_author is not None:
            recipe.author = recipe_author
        if recipe_name is not None:
            recipe.recipe_name = recipe_name
        if recipe_type is not None:
            recipe.recipe_type = recipe_type
        if ingredients_needed is not None:
            recipe.ingredients_needed = ingredients_needed
        if recipe_instructions is not None:
            recipe.recipe_instructions = recipe_instructions
        if prep_time_in_hours is not None:
            recipe.prep_time_in_hours = prep_time_in_hours
        if prep_time_in_minutes is not None:
            recipe.prep_time_in_minutes = prep_time_in_minutes
        if cooking_temp is not None:
            recipe.cooking_temp = cooking_temp
        if servings is not None:
            recipe.servings = servings

        recipe.save()
        return recipe
    except ObjectDoesNotExist:
        return None

def remove_recipe(recipeid):
    try:
        recipe = RecipeData.objects.get(id=recipeid)
        recipe.delete()
        return True
    except ObjectDoesNotExist:
        return False