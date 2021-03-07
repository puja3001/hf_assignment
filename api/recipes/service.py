import json

from dal.models import Recipes, RecipeIngredients, Ingredients, Category, RecipeNutritionalValues, RecipeSteps
from errors import RecipeNotFound
from models.models import RecipeModel, Dict2Class


class RecipeService:
    def __init__(self, **kwargs):
        pass

    def get_recipe_list_by_category(self, categoryId):
        query = Recipes.select(Recipes, Category.name.alias('category')) \
            .join(Category).where(Recipes.categoryId == categoryId).namedtuples()
        response = []
        for row in query:
            response.append(row._asdict())
        return response

    def get_recipe_by_id(self, id):
        recipe_query = Recipes.select(Recipes, Category.name.alias('category')) \
            .join(Category).where(Recipes.recipeId == id).namedtuples()
        nutritional_values = RecipeNutritionalValues.select().where(
            RecipeNutritionalValues.recipeId == id).namedtuples()
        ing_query = RecipeIngredients.select(Ingredients.name, RecipeIngredients.quantity, RecipeIngredients.servesFour,
                                             RecipeIngredients.isDeliverable) \
            .join(Ingredients).where(RecipeIngredients.recipeId == id).namedtuples()
        steps_query = RecipeSteps.select().where(RecipeSteps.recipeId == id).order_by(RecipeSteps.stepNo).namedtuples()
        response = None
        for recipe in recipe_query:
            response = recipe._asdict()
            for nv in nutritional_values:
                response['nutritionalValues'] = nv._asdict()
            response['ingredients'] = []
            response['instructions'] = []
            for ing in ing_query:
                response['ingredients'].append(ing._asdict())
            for steps in steps_query:
                response['instructions'].append(steps._asdict())
        if response is None:
            raise RecipeNotFound("Recipe with the given id does not exist")
        return json.loads(json.dumps(response))

    def upsert_recipe(self, payload: RecipeModel):
        try:
            payload = Dict2Class(payload)
            recipe = {
                'recipeId': payload.recipeId,
                'name': payload.name,
                'description': payload.description,
                'allergens': payload.allergens,
                'prepTime': payload.prepTime,
                'difficultyLevel': payload.difficultyLevel,
                'tags': payload.tags,
                'categoryId': payload.categoryId
            }
            recipe = Recipes(**recipe)
            recipe.save()

            # updating nutritional values
            nutritional_values = {
                'recipeId': recipe.get_id(),
                **payload.nutritionalValues
            }
            RecipeNutritionalValues(**nutritional_values).save()

            # updating recipe ingredients
            for ingredient in payload.ingredients:
                recipe_ingredients = {
                    'recipeId': recipe.get_id(),
                    **ingredient
                }
                hasRows = RecipeIngredients.select().where(RecipeIngredients.recipeId == recipe.get_id(), RecipeIngredients.ingredientId == int(ingredient['ingredientId'])).count()
                if hasRows == 0:
                    RecipeIngredients(**recipe_ingredients).save(force_insert=True)
                else:
                    RecipeIngredients(**recipe_ingredients).save()

            # updating recipe steps
            for step in payload.instructions:
                recipe_steps = {
                    'recipeId': recipe.get_id(),
                    **step
                }
                RecipeSteps(**recipe_steps).save()

            return {
                "message": "Successfully upserted new recipe",
                "recipeId": recipe.get_id()
            }
        except Exception as ex:
            self.delete_recipe_records(payload.recipeId)

    def delete_recipe(self, id):
        self.delete_recipe_records(id)
        return {
            "message": "Successfully deleted recipe",
            "recipeId": id
        }

    def delete_recipe_records(self, id):
        if id is not None:
            RecipeSteps.delete().where(RecipeSteps.recipeId == id).execute()
            RecipeNutritionalValues.delete().where(RecipeNutritionalValues.recipeId == id).execute()
            RecipeIngredients.delete().where(RecipeIngredients.recipeId == id).execute()
            Recipes.delete().where(Recipes.recipeId == id).execute()
