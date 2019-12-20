from flask import Response , jsonify

class CustomResponse(Response):
    @classmethod
    def force_type(cls,value,environ = None):
        if isinstance(value,dict):
            value = jsonify(value)
        return super(CustomResponse ,cls).force_type(value,environ)

class CustomDatabaseException(Exception):
    def __init__(self):
        super().__init()
