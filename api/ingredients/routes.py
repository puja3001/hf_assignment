from flask import Blueprint, jsonify, request
from flask_restplus import abort
from werkzeug import Response
from config import logger
from errors import RecipeBeingUsed
from api.ingredients.service import IngredientService

igs = Blueprint(name="ingredient", import_name=__name__)
service = IngredientService()


@igs.route('/list/<category>', methods=['GET'])
def get_ingredient_list_by_category(category):
    try:
        values = service.get_ingredient_list_by_category(category)
        return jsonify(values)
    except Exception as ex:
        logger.error("Error occurred, request: {0}, error: {1}".format(request.full_path, str(ex)))
        abort(400, "Error occurred in operation" + str(ex))


@igs.route('/create', methods=['POST'])
def create_ingredient():
    try:
        data = request.get_json()
        values = service.create_ingredient(data)
        return jsonify(values)
    except Exception as ex:
        logger.error("Error occurred, request: {0}, error: {1}".format(request.full_path, str(ex)))
        abort(400, "Error occurred in operation" + str(ex))


@igs.route('/update', methods=['PUT'])
def update_ingredient():
    try:
        data = request.get_json()
        values = service.update_ingredient(data)
        return jsonify(values)
    except RecipeBeingUsed as ex:
        logger.warn("Recipe in use, request: {0}, error: {1}".format(request.full_path, str(ex)))
        return Response(str(ex), mimetype="text/plain", status=400)
    except Exception as ex:
        logger.error("Error occurred, request: {0}, error: {1}".format(request.full_path, str(ex)))
        abort(400, "Error occurred in operation" + str(ex))


@igs.route('/<id>', methods=['DELETE'])
def delete_recipe(id):
    try:
        values = service.delete_ingredient(id)
        return jsonify(values)
    except RecipeBeingUsed as ex:
        logger.error("Recipe in use, request: {0}, error: {1}".format(request.full_path, str(ex)))
        return Response(str(ex), mimetype="text/plain", status=400)
    except Exception as ex:
        logger.error("Error occurred, request: {0}, error: {1}".format(request.full_path, str(ex)))
        abort(400, "Error occurred in operation" + str(ex))
