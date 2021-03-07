import json

from dal.models import RecipeIngredients, Ingredients
from tests.base import setup_db, clean_db


class TestIngredientClass:
    @classmethod
    def setup_class(self):
        setup_db()

    @classmethod
    def teardown_class(self):
        clean_db()

    def test_get_ingredients_by_category(self, app, client):
        res = client.get('/api/v1/ingredients/list/Dairy')
        assert res.status_code == 401

        headers = {'x-api-key': 'test'}
        res = client.get('/api/v1/ingredients/list/Dairy', headers=headers)
        response = res.get_json()
        assert res.status_code == 200
        assert len(response) == 2

        res = client.get('/api/v1/ingredients/list/Fruits', headers=headers)
        response = res.get_json()
        assert res.status_code == 200
        assert len(response) == 0

    def test_create_ingredient(self, app, client):
        data = {
            "name": "potatoes",
            "category": "Veggies"
        }
        headers = {'x-api-key': 'test'}
        res = client.post('/api/v1/ingredients/create', mimetype="application/json", data=json.dumps(data),
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
        res = client.put('/api/v1/ingredients/update', mimetype="application/json", data=json.dumps(data),
                         headers=headers)
        assert res.status_code == 200
        response = res.get_json()
        assert response['message'] == "Successfully updated ingredient"
        ingredient = Ingredients.get_by_id(created.ingredientId)
        assert ingredient.category == "Farm-fruits"

        used_ingredient = RecipeIngredients.select(RecipeIngredients.ingredientId).limit(1)
        for rows in used_ingredient:
            data = {
                "ingredientId": 2,
                "name": "apple",
                "category": "Farm-fruits"
            }
            print(data)
            res = client.put('/api/v1/ingredients/update', mimetype="application/json", data=json.dumps(data),
                             headers=headers)
            assert res.status_code == 400

    def test_delete_ingredient(self, app, client):
        created = Ingredients.create(name="apple-new", category="fruits")

        headers = {'x-api-key': 'test'}
        res = client.delete('/api/v1/ingredients/' + str(created.ingredientId), mimetype="application/json",
                            headers=headers)
        assert res.status_code == 200
        response = res.get_json()
        assert response['message'] == "Successfully deleted ingredient"
        ingredient = Ingredients.select().where(Ingredients.ingredientId == created.ingredientId).count()
        assert ingredient == 0

        used_ingredient = RecipeIngredients.select().limit(1)
        for rows in used_ingredient:
            res = client.delete('/api/v1/ingredients/' + str(rows.ingredientId), mimetype="application/json",
                                headers=headers)
            assert res.status_code == 400
