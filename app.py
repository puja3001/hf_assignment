from flask import Flask
from flask_restplus import Api

from api.ingredients.routes import igs
from api.recipes.routes import rs
from api.reviews.routes import rvs
from api.weeklymenu.routes import wms
from middleware.authentication import Authentication


def register_blueprints(app):
    app.register_blueprint(rs, url_prefix="/api/v1/recipes")
    app.register_blueprint(igs, url_prefix="/api/v1/ingredients")
    app.register_blueprint(wms, url_prefix="/api/v1/weeklymenus")
    app.register_blueprint(rvs, url_prefix="/api/v1/reviews")


def create_app():
    app = Flask(__name__)
    api = Api(app)
    app.wsgi_app = Authentication(app.wsgi_app)
    register_blueprints(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
