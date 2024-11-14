from django import forms
from app.models import RecipeData


class NewRecipeCreation(forms.Form):
    recipe_author = forms.CharField(max_length=75)
    recipe_name = forms.CharField(max_length=75)
    recipe_type = forms.CharField(max_length=15, required=False)
    ingredients_needed = forms.CharField(max_length=600)
    recipe_instructions = forms.CharField(max_length=1200)
    prep_time_in_minutes = forms.IntegerField(required=False)
    prep_time_in_hours = forms.IntegerField(required=False)
    cooking_temp = forms.IntegerField(required=False)
    servings = forms.IntegerField(required=False)







