from dal.models import RecipeIngredients, Ingredients
from errors import RecipeBeingUsed
from models.models import IngredientModel


class IngredientService:
    def __init__(self, **kwargs):
        pass

    def get_ingredient_list_by_category(self, category):
        query = Ingredients.select().where(Ingredients.category == category.lower()).namedtuples()
        response = []
        for row in query:
            response.append(row._asdict())
        return response

    def create_ingredient(self, payload: IngredientModel):
        payload['category'] = payload['category'].lower() if payload['category'] else None
        ingredient = Ingredients.create(**payload)
        return {
            "message": "Successfully created new ingredient",
            "ingredientId": ingredient.ingredientId
        }

    def update_ingredient(self, payload: IngredientModel):
        recipes = RecipeIngredients.select().where(RecipeIngredients.ingredientId == payload['ingredientId']).count()
        if recipes > 0:
            raise RecipeBeingUsed("Cannot update ingredient as its been referenced in {0} recipes.".format(recipes))

        payload['category'] = payload['category'].lower() if payload['category'] else None
        ingredient = Ingredients(**payload).save()
        return {
            "message": "Successfully updated ingredient"
        }


    def delete_ingredient(self, id):
        recipes = RecipeIngredients.select().where(RecipeIngredients.ingredientId == id).count()
        if recipes > 0:
            raise RecipeBeingUsed("Cannot delete ingredient as its been referenced in {0} recipes".format(recipes))
        Ingredients.delete().where(Ingredients.ingredientId == id).execute()
        return {
            "message": "Successfully deleted ingredient",
            "ingredientId": id
        }