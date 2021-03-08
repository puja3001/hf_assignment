import datetime
import json

from peewee import fn

from dal.models import Recipes, WeeklyMenu, Category
from errors import RecipeNotFound
from models.models import WeeklyMenuModel, Dict2Class
from utils import dateconverter
from config import config


class WeeklyMenuService:
    MAX_RECIPES_PER_MENU = config['max_no_of_recipes']

    def __init__(self, **kwargs):
        pass

    def get_weeklymenu_list_by_category(self, categoryId):
        '''
        List all weekly mneus by categoryId
        :param categoryId:
        :return:
        '''
        query = WeeklyMenu.select().where(WeeklyMenu.categoryId == categoryId).namedtuples()
        response = []
        for row in query:
            menu = row._asdict()
            menu['recipes'] = self.fetch_menu_recipes(menu)
            response.append(menu)

        return response

    def get_weekly_menu(self, menuId):
        '''
        Retrieves a menu by id
        :param menuId:
        :return:
        '''
        query = WeeklyMenu.select(WeeklyMenu, Category.name.alias('category')).join(Category).where(
            WeeklyMenu.menuId == menuId).namedtuples()
        response = {}
        for row in query:
            response = row._asdict()
        response = json.loads(json.dumps(response, default=dateconverter))
        response['recipes'] = self.fetch_menu_recipes(response)
        return json.loads(json.dumps(response))

    def fetch_menu_recipes(self, menu: WeeklyMenuModel):
        '''
        Fetch menu recipes
        :param menu:
        :return:
        '''
        recipes = []
        menu_recipes = Recipes.select().where(Recipes.recipeId.in_(menu['availableRecipes'].split(","))).namedtuples()
        for recipe in menu_recipes:
            recipes.append(recipe._asdict())
        return recipes

    def create_weekly_menu(self, payload: WeeklyMenuModel):
        '''
        Ceates a menu
        :param payload:
        :return:
        '''
        payload = Dict2Class(payload)
        week_start_date = datetime.datetime.strptime(payload.weekStartDate, '%Y-%m-%d')
        week_name = str(week_start_date.year) + "-W" + str(week_start_date.isocalendar()[1])

        # fetching previous week recipes from same category
        last_week_start = week_start_date - datetime.timedelta(days=7)
        query = WeeklyMenu.select().where(
            WeeklyMenu.weekStartDate == last_week_start and WeeklyMenu.categoryId == payload.categoryId).namedtuples()
        previous_week_menu = {}
        for row in query:
            previous_week_menu = row._asdict()
        previous_week_recipes = previous_week_menu['availableRecipes'].split(",")

        # assigning random x recipes to current menu from given category and which were not in previous week
        recipes = Recipes.select(Recipes.recipeId).where(
            Recipes.recipeId.not_in(previous_week_recipes), Recipes.categoryId == payload.categoryId) \
            .order_by(fn.Random()).limit(self.MAX_RECIPES_PER_MENU)
        available_recipes = []
        for recipe in recipes:
            available_recipes.append(str(recipe.recipeId))
        available_recipes = ",".join(available_recipes)
        weeklyMenu = WeeklyMenu(
            **{"categoryId": payload.categoryId, "weekName": week_name, "weekStartDate": week_start_date,
               "availableRecipes": available_recipes})
        weeklyMenu.save()
        return {
            "message": "Successfully created weekly menu",
            "menuId": weeklyMenu.get_id(),
            "week": week_name
        }

    def update_weekly_menu(self, payload: WeeklyMenuModel):
        '''
        Updates a menu
        :param payload:
        :return:
        '''
        payload = Dict2Class(payload)
        available_recipes = payload.availableRecipes.split(",")
        recipes = Recipes.select(Recipes.recipeId).where(Recipes.recipeId.in_(available_recipes)).count()
        if recipes < len(available_recipes):
            raise RecipeNotFound("Unable to update menu as some recipes are missing in database");

        updated = WeeklyMenu.update(availableRecipes=payload.availableRecipes).where(
            WeeklyMenu.menuId == payload.menuId).execute()
        return {
            "message": "Successfully updated weekly menu",
        }

    def delete_weekly_menu(self, menuId):
        '''
        Deletes a menu
        :param menuId:
        :return:
        '''
        deleted = WeeklyMenu.delete().where(WeeklyMenu.menuId == menuId).execute()
        return {
            "message": "Successfully deleted weekly menu",
            "menuId": menuId
        }
