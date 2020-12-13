import json

from flask import Response, jsonify


class ApiResponse(Response):

    defmimetype = 'application/json'

    def __init__(self,result,status,mimetype=None,error=None):
        if mimetype is not None:
            self.defmimetype = mimetype
        return super(ApiResponse, self).__init__(status=status,response=json.dumps({'result':result,'status':status,'error':error}),mimetype=self.defmimetype)

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(ApiResponse, cls).force_type(rv, environ)
