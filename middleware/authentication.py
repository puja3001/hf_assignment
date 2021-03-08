from werkzeug import Response
from config import config


class Authentication:
    def __init__(self, app):
        self.app = app
        self.secret_key = config['apiKey']

    def __call__(self, environ, start_response):
        '''
        Takes a incoming request to check for secret api key
        :param environ:
        :param start_response:
        :return:
        '''
        try:
            secret_key = environ.get("HTTP_X_API_KEY")
            if not secret_key or secret_key != self.secret_key:
                res = Response("Not Authorized", mimetype="text/plain", status=401)
                return res(environ, start_response)

        except Exception as ex:
            res = Response("Not Authorized", mimetype="text/plain", status=401)
            return res(environ, start_response)

        return self.app(environ, start_response)
