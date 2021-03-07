from flask import Blueprint, jsonify, request
from flask_restplus import abort

from api.reviews.service import ReviewService
from config import logger

rvs = Blueprint(name="review", import_name=__name__)
service = ReviewService()


@rvs.route('/menu/<id>', methods=['GET'])
def get_reviews_for_menu(id):
    try:
        values = service.get_reviews_for_menu(id)
        return jsonify(values)
    except Exception as ex:
        logger.error("Error occurred, request: {0}, error: {1}".format(request.full_path, str(ex)))
        abort(400, "Error occurred in operation" + str(ex))


@rvs.route('/recipe/<id>', methods=['GET'])
def get_reviews_for_recipe(id):
    try:
        values = service.get_reviews_for_recipe(id)
        return jsonify(values)
    except Exception as ex:
        logger.error("Error occurred, request: {0}, error: {1}".format(request.full_path, str(ex)))
        abort(400, "Error occurred in operation" + str(ex))


@rvs.route('/create', methods=['POST', 'PUT'])
def add_review():
    try:
        data = request.get_json()
        values = service.add_review(data)
        return jsonify(values)
    except Exception as ex:
        logger.error("Error occurred, request: {0}, error: {1}".format(request.full_path, str(ex)))
        abort(400, "Error occurred in operation" + str(ex))


@rvs.route('/<id>', methods=['DELETE'])
def delete_review(id):
    try:
        values = service.delete_review(id)
        return jsonify(values)
    except Exception as ex:
        logger.error("Error occurred, request: {0}, error: {1}".format(request.full_path, str(ex)))
        abort(400, "Error occurred in operation" + str(ex))