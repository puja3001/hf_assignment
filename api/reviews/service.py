from dal.models import UserReviews
from models.models import ReviewModel


class ReviewService:
    def __init__(self, **kwargs):
        pass

    def get_reviews_for_menu(self, menuId):
        '''
        List all reviews for a menu
        :param menuId:
        :return:
        '''
        print(menuId)
        query = UserReviews.select().where(UserReviews.menuId == menuId).namedtuples()
        print(query)
        response = []
        for row in query:
            menu = row._asdict()
            response.append(menu)

        return response

    def get_reviews_for_recipe(self, recipeId):
        '''
        List all reviews for a recipe
        :param recipeId:
        :return:
        '''
        query = UserReviews.select().where(UserReviews.recipeId == recipeId).namedtuples()
        response = []
        for row in query:
            menu = row._asdict()
            response.append(menu)

        return response

    def add_review(self, payload: ReviewModel):
        '''
        Creates/updates a review
        :param payload:
        :return:
        '''
        print(payload)
        created = UserReviews(**payload).save()
        return {
            "message": "Successfully added review"
        }

    def delete_review(self, reviewId):
        '''
        Deletes a review by id
        :param reviewId:
        :return:
        '''
        deleted = UserReviews.delete().where(UserReviews.reviewId == reviewId).execute()
        return {
            "message": "Successfully deleted review"
        }

