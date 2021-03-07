import json
import os

from dal.models import Category, WeeklyMenu, RecipeNutritionalValues, RecipeIngredients, Recipes, Ingredients, \
    RecipeSteps, UserReviews, database_proxy

base_dir = os.path.dirname(__file__)
filename = os.path.join(base_dir, 'fixtures', 'data.json')


def drop_tables():
    with database_proxy.connection_context():
        UserReviews.truncate_table(restart_identity=True)
        RecipeSteps.truncate_table(restart_identity=True)
        Ingredients.truncate_table(restart_identity=True)
        Recipes.truncate_table(restart_identity=True)
        RecipeIngredients.truncate_table(restart_identity=True)
        RecipeNutritionalValues.truncate_table(restart_identity=True)
        WeeklyMenu.truncate_table(restart_identity=True)
        Category.truncate_table(restart_identity=True)


def create_tables():
    with database_proxy.connection_context():
        print(database_proxy)
        Category.create_table(safe=True)
        Ingredients.create_table(safe=True)
        Recipes.create_table(safe=True)
        RecipeNutritionalValues.create_table(safe=True)
        RecipeIngredients.create_table(safe=True)
        RecipeSteps.create_table(safe=True)
        WeeklyMenu.create_table(safe=True)
        UserReviews.create_table(safe=True)


def insert_values():
    file = open(filename)
    data_source = json.load(file)
    with database_proxy.atomic():
        for data_dict in data_source['category']:
            Category.create(**data_dict)
        for data_dict in data_source['ingredients']:
            Ingredients.create(**data_dict)
        for data_dict in data_source['recipes']:
            Recipes.create(**data_dict)
        for data_dict in data_source['recipe_nutritional_values']:
            RecipeNutritionalValues.create(**data_dict)
        for data_dict in data_source['recipe_steps']:
            RecipeSteps.create(**data_dict)
        for data_dict in data_source['recipe_ingredients']:
            RecipeIngredients.create(**data_dict)
        for data_dict in data_source['weekly_menu']:
            WeeklyMenu.create(**data_dict)
        for data_dict in data_source['user_reviews']:
            UserReviews.create(**data_dict)


if __name__ == '__main__':
    drop_tables()
    create_tables()
    insert_values()
