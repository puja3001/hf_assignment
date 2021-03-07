import json
import os

from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
from config import config

database_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = database_proxy


class Category(BaseModel):
    categoryId = AutoField
    name = CharField()

    class Meta:
        table_name = 'category'


class Ingredients(BaseModel):
    ingredientId = AutoField()
    name = CharField()
    category = CharField(null=True)

    class Meta:
        table_name = 'ingredients'


class Recipes(BaseModel):
    recipeId = AutoField()
    name = CharField()
    description = CharField(null=True)
    categoryId = ForeignKeyField(Category, column_name='categoryId')
    tags = CharField(null=True)
    prepTime = CharField()
    difficultyLevel = CharField()
    allergens = CharField(null=True)

    class Meta:
        table_name = 'recipes'


class RecipeNutritionalValues(BaseModel):
    nutritionId = AutoField()
    energy = CharField()
    fat = CharField(null=True)
    saturates = CharField(null=True)
    carbohydrates = CharField(null=True)
    sugar = CharField(null=True)
    fibre = CharField(null=True)
    protein = CharField(null=True)
    sodium = CharField(null=True)
    recipeId = ForeignKeyField(Recipes, column_name='recipeId')

    class Meta:
        table_name = 'recipe_nutritional_values'


class RecipeSteps(BaseModel):
    stepId = AutoField()
    recipeId = ForeignKeyField(Recipes, column_name='recipeId')
    stepNo = IntegerField()
    description = TextField()

    class Meta:
        table_name = 'recipe_steps'


class RecipeIngredients(BaseModel):
    recipeId = ForeignKeyField(Recipes, column_name='recipeId')
    ingredientId = ForeignKeyField(Ingredients, column_name='ingredientId')
    quantity = CharField()
    servesFour = BooleanField()
    isDeliverable = BooleanField()

    class Meta:
        table_name = 'recipe_ingredients'
        primary_key = CompositeKey('recipeId', 'ingredientId')


class WeeklyMenu(BaseModel):
    menuId = AutoField()
    weekName = CharField()
    categoryId = ForeignKeyField(Category, column_name='categoryId')
    weekStartDate = DateField()
    availableRecipes = CharField()

    class Meta:
        table_name = 'weekly_menu'


class UserReviews(BaseModel):
    reviewId = AutoField()
    menuId = ForeignKeyField(WeeklyMenu, column_name='menuId', null=True)
    recipeId = ForeignKeyField(Recipes, column_name='recipeId', null=True)
    comments = TextField(null=True)
    rating = IntegerField(null=True)

    class Meta:
        table_name = 'user_reviews'


# Based on configuration, use a different database.
MODELS = (
Ingredients, Category, Recipes, RecipeNutritionalValues, RecipeSteps, RecipeIngredients, WeeklyMenu, UserReviews)

if os.environ.get("env") == "test":
    database = SqliteExtDatabase(":memory:")
    database_proxy.initialize(database)
    database_proxy.bind(MODELS, bind_refs=False, bind_backrefs=False)
    database_proxy.connect()

else:
    db_connection = config['db_connection']
    database = PostgresqlDatabase(
        db_connection['database'],
        user=db_connection['user'],
        password=db_connection['password'],
        host=db_connection['host']
    )
    database_proxy.initialize(database)


def create_tables():
    database_proxy.create_tables(MODELS)


def insert_values(filepath):
    file = open(filepath)
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
