from flask import make_response
from flask_restplus import Namespace
from flask_restplus import Resource
 
endpoint = Namespace('healthcheck')

@endpoint.route("/", strict_slashes=False)
@endpoint.response(200, "the service is up")
class HealthCheck(Resource):

    def get(self):  
        """    
        API health check
        """             
        return "aa", 200