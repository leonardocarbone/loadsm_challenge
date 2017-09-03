from flask import make_response
from flask_restplus import Namespace
from flask_restplus import Resource
 
endpoint = Namespace('healthcheck')

@endpoint.route("/")
@endpoint.response(200, "the service is up")
class HealthCheck(Resource):

    def get(self):  
        """    
        API health check
        """             
        response = make_response("")
        response.headers['Content-Type'] = "text/plain"
        return response