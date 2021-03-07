import json

from config import config
from dal.models import WeeklyMenu, UserReviews
from tests.base import setup_db, clean_db


class TestUSerReviewClass:
    URL_PREFIX = '/api/v1/reviews'

    @classmethod
    def setup_class(self):
        setup_db()

    @classmethod
    def teardown_class(self):
        clean_db()

    def test_get_reviews_for_menu(self, app, client):
        res = client.get("{0}{1}".format(self.URL_PREFIX, '/menu/1'))
        assert res.status_code == 401

        headers = {'x-api-key': 'test'}
        res = client.get("{0}{1}".format(self.URL_PREFIX, '/menu/1'), headers=headers)
        response = res.get_json()
        assert res.status_code == 200
        assert len(response) == 1

        res = client.get("{0}{1}".format(self.URL_PREFIX, '/menu/4'), headers=headers)
        response = res.get_json()
        assert res.status_code == 200
        assert len(response) == 0

    def test_get_reviews_for_recipe(self, app, client):
        res = client.get("{0}{1}".format(self.URL_PREFIX, '/recipe/3'))
        assert res.status_code == 401

        headers = {'x-api-key': 'test'}
        res = client.get("{0}{1}".format(self.URL_PREFIX, '/recipe/3'), headers=headers)
        response = res.get_json()
        assert res.status_code == 200
        assert len(response) == 2

        res = client.get("{0}{1}".format(self.URL_PREFIX, '/recipe/1'), headers=headers)
        response = res.get_json()
        assert res.status_code == 200
        assert len(response) == 0

    def test_create_review(self, app, client):
        data = {
            "comments": "Fantastic recipe",
            "ratings": 5,
            "recipeId": 1
        }

        headers = {'x-api-key': 'test'}
        res = client.post("{0}{1}".format(self.URL_PREFIX, '/create'), mimetype="application/json",
                          data=json.dumps(data), headers=headers)
        response = res.get_json()
        assert res.status_code == 200
        assert response["message"] == "Successfully added review"
        reviews = UserReviews.select().where(UserReviews.reviewId == 1).count()
        assert reviews > 0

    def test_update_review(self, app, client):
        data = {
            "comments": "Fantastic recipe",
            "rating": 5,
            "reviewId": 1,
            "recipeId": 1
        }

        headers = {'x-api-key': 'test'}
        res = client.put("{0}{1}".format(self.URL_PREFIX, '/create'), mimetype="application/json",
                         data=json.dumps(data), headers=headers)
        response = res.get_json()
        assert res.status_code == 200
        assert response["message"] == "Successfully added review"

        reviews = UserReviews.select().where(UserReviews.recipeId == 1).count()
        review = UserReviews.get_by_id(1)
        assert reviews > 0
        assert review.rating == 5
        assert review.comments == "Fantastic recipe"

    def test_delete_review(self, app, client):
            headers = {'x-api-key': 'test'}
            res = client.delete("{0}{1}".format(self.URL_PREFIX, '/1'), mimetype="application/json", headers=headers)
            response = res.get_json()
            assert res.status_code == 200
            assert response["message"] == "Successfully deleted review"

            reviews = UserReviews.select().where(UserReviews.reviewId == 1).count()
            assert reviews == 0
