from flask import Blueprint, jsonify, request
from flask_restplus import abort
from api.recipes.service import RecipeService
from config import logger

rs = Blueprint(name="recipe", import_name=__name__)
service = RecipeService()


@rs.route('/list/<categoryId>', methods=['GET'])
def get_recipe_list_by_category(categoryId):
    try:
        values = service.get_recipe_list_by_category(categoryId)
        return jsonify(values)
    except Exception as ex:
        logger.error("Error occurred, request: {0}, error: {1}".format(request.full_path, str(ex)))
        abort(400, "Error occurred in operation" + str(ex))


@rs.route('/<id>', methods=['GET'])
def get_recipe_by_id(id):
    try:
        values = service.get_recipe_by_id(id)
        return jsonify(values)
    except Exception as ex:
        logger.error("Error occurred, request: {0}, error: {1}".format(request.full_path, str(ex)))
        abort(400, "Error occurred in operation" + str(ex))


@rs.route('/create', methods=['POST', 'PUT'])
def upsert_recipe():
    try:
        data = request.get_json()
        values = service.upsert_recipe(data)
        return jsonify(values)
    except Exception as ex:
        logger.error("Error occurred, request: {0}, error: {1}".format(request.full_path, str(ex)))
        abort(400, "Error occurred in operation" + str(ex))


@rs.route('/<id>', methods=['DELETE'])
def delete_recipe(id):
    try:
        values = service.delete_recipe(id)
        return jsonify(values)
    except Exception as ex:
        logger.error("Error occurred, request: {0}, error: {1}".format(request.full_path, str(ex)))
        abort(400, "Error occurred in operation" + str(ex))
