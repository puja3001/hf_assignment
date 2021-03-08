from flask import Blueprint, jsonify, request
from flask_restplus import abort
from werkzeug import Response
from config import logger
from errors import RecipeNotFound
from api.weeklymenu.service import WeeklyMenuService

wms = Blueprint(name="weeklymenu", import_name=__name__)
service = WeeklyMenuService()


@wms.route('/list/<categoryId>', methods=['GET'])
def get_ingredient_list_by_category(categoryId):
    try:
        values = service.get_weeklymenu_list_by_category(categoryId)
        return jsonify(values)
    except Exception as ex:
        logger.error("Error occurred, request: {0}, error: {1}".format(request.full_path, str(ex)))
        abort(400, "Error occurred in operation" + str(ex))


@wms.route('/<id>', methods=['GET'])
def get_weekly_menu(id):
    try:
        values = service.get_weekly_menu(id)
        return jsonify(values)
    except Exception as ex:
        logger.error("Error occurred, request: {0}, error: {1}".format(request.full_path, str(ex)))
        abort(400, "Error occurred in operation" + str(ex))


@wms.route('/create', methods=['POST'])
def create_weekly_menu():
    try:
        data = request.get_json()
        values = service.create_weekly_menu(data)
        return jsonify(values)
    except Exception as ex:
        logger.error("Error occurred, request: {0}, error: {1}".format(request.full_path, str(ex)))
        abort(400, "Error occurred in operation" + str(ex))


@wms.route('/update', methods=['PUT'])
def update_weekly_menu():
    try:
        data = request.get_json()
        values = service.update_weekly_menu(data)
        return jsonify(values)
    except RecipeNotFound as ex:
        logger.error("Recipe not found, request: {0}, error: {1}".format(request.full_path, str(ex)))
        return Response(str(ex), mimetype="text/plain", status=400)
    except Exception as ex:
        logger.error("Error occurred, request: {0}, error: {1}".format(request.full_path, str(ex)))
        abort(400, "Error occurred in operation" + str(ex))


@wms.route('/<id>', methods=['DELETE'])
def delete_weekly_menu(id):
    try:
        values = service.delete_weekly_menu(id)
        return jsonify(values)
    except Exception as ex:
        logger.error("Error occurred, request: {0}, error: {1}".format(request.full_path, str(ex)))
        abort(400, "Error occurred in operation" + str(ex))