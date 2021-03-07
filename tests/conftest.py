import os

import pytest
from app import create_app

from dal.models import Ingredients, Category, RecipeNutritionalValues, Recipes, RecipeSteps, RecipeIngredients, \
    WeeklyMenu, UserReviews, insert_values, create_tables, drop_tables
from tests import helpers

MODELS = (
    Ingredients, Category, Recipes, RecipeNutritionalValues, RecipeSteps, RecipeIngredients, WeeklyMenu, UserReviews)

os.environ.__setitem__('ENV', 'test')


@pytest.fixture
def app():
    yield create_app()


@pytest.fixture
def recipe_response():
    test_data = helpers.load_fixtures('recipes.json')
    return test_data['Recipe-Response']


@pytest.fixture
def recipe_payload():
    test_data = helpers.load_fixtures('recipes.json')
    return test_data['Recipe-Payload']


@pytest.fixture
def recipe_record():
    test_data = helpers.load_fixtures('recipes.json')
    return test_data['Recipe-Record']


@pytest.fixture
def nutritional_value_record():
    test_data = helpers.load_fixtures('nutritionalValues.json')
    return test_data['RecipeNutritionalValue']


@pytest.fixture
def recipe_ingredient_record():
    test_data = helpers.load_fixtures('ingredients.json')
    return test_data


@pytest.fixture
def recipe_steps_record():
    test_data = helpers.load_fixtures('instructions.json')
    return test_data['RecipeSteps']
