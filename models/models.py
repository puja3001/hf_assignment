import json
from typing import List

DEFAULT_FIELDS = ["stepId", "recipeId", "ingredientId", "nutritionId", "reviewId", "menuId"]


class StepsModel:
    stepNo: int
    description: str
    stepId: int = None
    recipeId: int = None


class RecipeIngredientsModel(object):
    quantity: str
    servesFour: bool
    isDeliverable: bool
    ingredientId: int = None
    recipeId: int = None


class NutritionalValuesModel(object):
    carbohydrates: str
    energy: str
    fat: str
    fibre: str
    protein: str
    recipeId: str
    saturates: str
    sodium: str
    sugar: str
    nutritionId: int = None
    recipeId: int = None


class RecipeModel(object):
    name: str
    description: str
    category: str
    categoryId: int
    allergens: str
    difficultyLevel: str
    tags: str
    prepTime: str
    nutritionalValues: NutritionalValuesModel
    ingredients: List[RecipeIngredientsModel]
    instructions: List[StepsModel]
    recipeId: int = None


class IngredientModel(object):
    name: str
    category: str
    ingredientId: int = None


class WeeklyMenuModel(object):
    weekName = str
    categoryId = int
    weekStartDate = str
    availableRecipes = List[int]
    menuId = int = None


class ReviewModel(object):
    comments = str
    rating = int
    reviewId = int = None
    menuId = int = None
    recipeId = int = None


class Dict2Class(object):
    def __init__(self, dict):
        keys = dict.keys()
        temp = [x for x in DEFAULT_FIELDS if x not in keys]
        for key in temp:
            setattr(self, key, None)
        for key in dict:
            setattr(self, key, dict[key])
