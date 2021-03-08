import json

from dal.models import Recipes, RecipeSteps, RecipeNutritionalValues, RecipeIngredients, Ingredients, Category
from tests.base import setup_db, clean_db


class TestRecipeClass:
    URL_PREFIX = '/api/v1/recipes'

    @classmethod
    def setup_class(self):
        setup_db()

    @classmethod
    def teardown_class(self):
        clean_db()

    def test_get_recipe_list_by_category(self, app, client):
        # test if response is returned as unauthorized when no token is passed
        res = client.get("{0}{1}".format(self.URL_PREFIX, '/list/1'))
        assert res.status_code == 401

        # test if recipes are listed correctly as per category
        headers = {'x-api-key': 'test'}
        res = client.get("{0}{1}".format(self.URL_PREFIX, '/list/1'), headers=headers)
        response = res.get_json()
        assert res.status_code == 200

        # test if actual count of recipes in database is same as the one returned
        count = Recipes.select().where(Recipes.categoryId == 1).count()
        assert len(response) == count

    def test_get_recipe(self, app, client, recipe_response):
        # test if recipe is listed successfully
        headers = {'x-api-key': 'test'}
        res = client.get("{0}{1}".format(self.URL_PREFIX, '/1'), mimetype="application/json", headers=headers)

        response = res.get_json()
        assert res.status_code == 200

        # test if recipe metadata is same as the one passed in the response
        assert response['recipeId'] == 1
        assert len(response['ingredients']) == 14
        assert len(response['instructions']) == 6

        # test if no recipe is returned is no recipe id exists
        res = client.get("{0}{1}".format(self.URL_PREFIX, '/78'), mimetype="application/json", headers=headers)
        assert res.status_code == 400

    def test_create_new_recipe(self, app, client, recipe_payload):
        # test if recipe is created successfully
        headers = {'x-api-key': 'test'}
        res = client.post("{0}{1}".format(self.URL_PREFIX, '/create'), mimetype="application/json",
                          data=json.dumps(recipe_payload),
                          headers=headers)

        response = res.get_json()
        assert res.status_code == 200
        assert response['message'] == "Successfully upserted new recipe"
        assert response['recipeId'] is not None

        # test if recipe metadata is same as the one passed in the request
        recipe = Recipes.get_by_id(response['recipeId'])
        nv_created = RecipeNutritionalValues.get(RecipeNutritionalValues.recipeId == recipe.recipeId)
        steps = RecipeSteps.select().where(RecipeSteps.recipeId == recipe.recipeId).count()
        ingredients = RecipeIngredients.select().where(RecipeIngredients.recipeId == recipe.recipeId).count()

        assert recipe.name == recipe_payload['name']
        assert nv_created is not None
        assert steps == 6
        assert ingredients == 3
        assert recipe.tags == "New"

    def test_delete_recipe(self, app, client):
        # test if recipe is deleted successfully
        headers = {'x-api-key': 'test'}
        res = client.delete("{0}{1}".format(self.URL_PREFIX, '/1'), mimetype="application/json", headers=headers)

        response = res.get_json()
        assert res.status_code == 200
        assert response['recipeId'] == '1'

        # test if recipe and its metadata is actually deleted from database
        deleted = Recipes.select().where(Recipes.recipeId == int(response['recipeId'])).count()
        nv_deleted = RecipeNutritionalValues.select().where(
            RecipeNutritionalValues.recipeId == int(response['recipeId'])).count()
        ig_deleted = RecipeIngredients.select().where(RecipeIngredients.recipeId == int(response['recipeId'])).count()
        s_deleted = RecipeSteps.select().where(RecipeSteps.recipeId == int(response['recipeId'])).count()
        assert deleted == 0
        assert nv_deleted == 0
        assert ig_deleted == 0
        assert s_deleted == 0
