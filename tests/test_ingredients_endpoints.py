import json

from dal.models import RecipeIngredients, Ingredients
from tests.base import setup_db, clean_db


class TestIngredientClass:
    URL_PREFIX = '/api/v1/ingredients'

    @classmethod
    def setup_class(self):
        setup_db()

    @classmethod
    def teardown_class(self):
        clean_db()

    def test_get_ingredients_by_category(self, app, client):

        # test if response is returned as unauthorized when no token is passed
        res = client.get("{0}{1}".format(self.URL_PREFIX, '/list/Dairy'))
        assert res.status_code == 401

        # test ingredients are listed as per category
        headers = {'x-api-key': 'test'}
        res = client.get("{0}{1}".format(self.URL_PREFIX, '/list/Dairy'), headers=headers)
        response = res.get_json()
        assert res.status_code == 200
        assert len(response) == 2

        # test ingredients are listed as per category
        res = client.get("{0}{1}".format(self.URL_PREFIX, '/list/Fruits'), headers=headers)
        response = res.get_json()
        assert res.status_code == 200
        assert len(response) == 0

    def test_create_ingredient(self, app, client):

        # test ingredient is created successfully
        data = {
            "name": "potatoes",
            "category": "Veggies"
        }
        headers = {'x-api-key': 'test'}
        res = client.post("{0}{1}".format(self.URL_PREFIX, '/create'), mimetype="application/json",
                          data=json.dumps(data),
                          headers=headers)
        response = res.get_json()
        assert res.status_code == 200
        assert response['message'] == "Successfully created new ingredient"
        assert response['ingredientId'] is not None

        # test the created ingredient as correct name as passed in payload
        ingredient = Ingredients.get_by_id(response['ingredientId'])
        assert ingredient.name == "potatoes"

    def test_update_ingredient(self, app, client):

        # test ingredients are updated correctly
        created = Ingredients.create(name="apple", category="Fruits")
        data = {
            "ingredientId": created.ingredientId,
            "name": "apple",
            "category": "Farm-fruits"
        }
        headers = {'x-api-key': 'test'}
        res = client.put("{0}{1}".format(self.URL_PREFIX, '/update'), mimetype="application/json",
                         data=json.dumps(data),
                         headers=headers)
        assert res.status_code == 200
        response = res.get_json()
        assert response['message'] == "Successfully updated ingredient"

        # test updated ingredient has the category updated as per payload
        ingredient = Ingredients.get_by_id(created.ingredientId)
        assert ingredient.category == "farm-fruits"

        # test ingredient is not updated if used in recipes
        used_ingredient = RecipeIngredients.select(RecipeIngredients.ingredientId).limit(1)
        for rows in used_ingredient:
            data = {
                "ingredientId": 2,
                "name": "apple",
                "category": "Farm-fruits"
            }
            res = client.put("{0}{1}".format(self.URL_PREFIX, '/update'), mimetype="application/json",
                             data=json.dumps(data),
                             headers=headers)
            assert res.status_code == 400

    def test_delete_ingredient(self, app, client):

        # test ingredients are deleted correctly
        created = Ingredients.create(name="apple-new", category="fruits")

        headers = {'x-api-key': 'test'}
        res = client.delete("{0}{1}".format(self.URL_PREFIX, "/{0}".format(created.ingredientId)),
                            mimetype="application/json",
                            headers=headers)
        assert res.status_code == 200
        response = res.get_json()
        assert response['message'] == "Successfully deleted ingredient"

        # test the ingredient is actually deleted from database
        ingredient = Ingredients.select().where(Ingredients.ingredientId == created.ingredientId).count()
        assert ingredient == 0

        # test ingredient is not deleted if used in recipes
        used_ingredient = RecipeIngredients.select().limit(1)
        for rows in used_ingredient:
            res = client.delete("{0}{1}".format(self.URL_PREFIX, "/{0}".format(rows.ingredientId)),
                                mimetype="application/json",
                                headers=headers)
            assert res.status_code == 400
