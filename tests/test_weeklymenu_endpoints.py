import json

from config import config
from dal.models import WeeklyMenu
from tests.base import setup_db, clean_db


class TestWeeklyMenuClass:

    URL_PREFIX = '/api/v1/weeklymenus'
    MAX_RECIPES_PER_MENU = config['max_no_of_recipes']

    @classmethod
    def setup_class(self):
        setup_db()

    @classmethod
    def teardown_class(self):
        clean_db()

    def test_get_menu_by_category(self, app, client):

        # test if response is returned as unauthorized if no token is passed
        res = client.get("{0}{1}".format(self.URL_PREFIX, '/list/1'))
        assert res.status_code == 401

        # test if weekly menus is listed correctly as per category id
        headers = {'x-api-key': 'test'}
        res = client.get("{0}{1}".format(self.URL_PREFIX, '/list/1'), headers=headers)
        response = res.get_json()
        assert res.status_code == 200
        assert len(response) == 1

        res = client.get("{0}{1}".format(self.URL_PREFIX, '/list/4'), headers=headers)
        response = res.get_json()
        assert res.status_code == 200
        assert len(response) == 0

    def test_create_weekly_menu(self, app, client):

        # test if weekly menu is created successfully
        data = {
            "weekStartDate": "2021-03-20",
            "categoryId": 2
        }
        headers = {'x-api-key': 'test'}
        res = client.post("{0}{1}".format(self.URL_PREFIX, '/create'), mimetype="application/json", data=json.dumps(data),
                          headers=headers)
        response = res.get_json()
        menu = WeeklyMenu.get_by_id(response['menuId'])
        assert res.status_code == 200
        assert response['message'] == "Successfully created weekly menu"
        assert response['menuId'] == menu.menuId

        # test if weekly menu weekname is populated correctly
        assert menu.weekName == "2021-W11"

        # test if available recipes count is as per the max allowed
        available_recipes = menu.availableRecipes.split(",")
        assert len(available_recipes) == self.MAX_RECIPES_PER_MENU

    def test_update_weekly_menu(self, app, client):

        # test if weekly menu is updated successfully
        headers = {'x-api-key': 'test'}
        data = {
            "menuId": 1,
            "availableRecipes": '1,2,3'
        }
        res = client.put("{0}{1}".format(self.URL_PREFIX, '/update'), mimetype="application/json", data=json.dumps(data), headers=headers)
        response = res.get_json()
        menu = WeeklyMenu.get_by_id(1)
        assert res.status_code == 200
        assert response['message'] == "Successfully updated weekly menu"
        assert menu.availableRecipes.split(",") == ['1', '2', '3']

        # test if weekly menu is not updated is recipe isd passed in not in recipe table
        data = {
            "menuId": '1',
            "availableRecipes": [4,5]
        }
        res = client.put("{0}{1}".format(self.URL_PREFIX, '/update'), mimetype="application/json", data=json.dumps(data),
                          headers=headers)
        assert res.status_code == 400

    def test_delete_weeklymenu(self, app, client):

        # test if weekly menu is deleted successfully
        headers = {'x-api-key': 'test'}
        res = client.delete("{0}{1}".format(self.URL_PREFIX, '/1'), mimetype="application/json", headers=headers)
        assert res.status_code == 200
        response = res.get_json()
        assert response['message'] == "Successfully deleted weekly menu"
        weeklyMenu = WeeklyMenu.select().where(WeeklyMenu.menuId == 1).count()
        assert weeklyMenu == 0
