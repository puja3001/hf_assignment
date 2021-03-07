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
        res = client.get("{0}{1}".format(self.URL_PREFIX, '/list/Dairy'))
        assert res.status_code == 401

        headers = {'x-api-key': 'test'}
        res = client.get("{0}{1}".format(self.URL_PREFIX, '/list/Dairy'), headers=headers)
        response = res.get_json()
        assert res.status_code == 200
        assert len(response) == 2

        res = client.get("{0}{1}".format(self.URL_PREFIX, '/list/Fruits'), headers=headers)
        response = res.get_json()
        assert res.status_code == 200
        assert len(response) == 0

    def test_create_ingredient(self, app, client):
        data = {
            "name": "potatoes",
            "category": "Veggies"
        }
        headers = {'x-api-key': 'test'}
        res = client.post("{0}{1}".format(self.URL_PREFIX, '/create'), mimetype="application/json", data=json.dumps(data),
                          headers=headers)
        response = res.get_json()
        assert res.status_code == 200
        assert response['message'] == "Successfully created new ingredient"
        assert response['ingredientId'] is not None

        ingredient = Ingredients.get_by_id(response['ingredientId'])
        assert ingredient.name == "potatoes"

    def test_update_ingredient(self, app, client):
        created = Ingredients.create(name="apple", category="Fruits")
        data = {
            "ingredientId": created.ingredientId,
            "name": "apple",
            "category": "Farm-fruits"
        }
        headers = {'x-api-key': 'test'}
        res = client.put("{0}{1}".format(self.URL_PREFIX, '/update'), mimetype="application/json", data=json.dumps(data),
                         headers=headers)
        assert res.status_code == 200
        response = res.get_json()
        assert response['message'] == "Successfully updated ingredient"
        ingredient = Ingredients.get_by_id(created.ingredientId)
        assert ingredient.category == "farm-fruits"

        used_ingredient = RecipeIngredients.select(RecipeIngredients.ingredientId).limit(1)
        for rows in used_ingredient:
            data = {
                "ingredientId": 2,
                "name": "apple",
                "category": "Farm-fruits"
            }
            res = client.put("{0}{1}".format(self.URL_PREFIX, '/update'), mimetype="application/json", data=json.dumps(data),
                             headers=headers)
            assert res.status_code == 400

    def test_delete_ingredient(self, app, client):
        created = Ingredients.create(name="apple-new", category="fruits")

        headers = {'x-api-key': 'test'}
        res = client.delete("{0}{1}".format(self.URL_PREFIX, "/{0}".format(created.ingredientId)), mimetype="application/json",
                            headers=headers)
        assert res.status_code == 200
        response = res.get_json()
        assert response['message'] == "Successfully deleted ingredient"
        ingredient = Ingredients.select().where(Ingredients.ingredientId == created.ingredientId).count()
        assert ingredient == 0

        used_ingredient = RecipeIngredients.select().limit(1)
        for rows in used_ingredient:
            res = client.delete("{0}{1}".format(self.URL_PREFIX, "/{0}".format(rows.ingredientId)), mimetype="application/json",
                                headers=headers)
            assert res.status_code == 400
