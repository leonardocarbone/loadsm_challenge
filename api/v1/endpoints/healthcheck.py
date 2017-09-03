from flask import make_response
from flask_restplus import Namespace
from flask_restplus import Resource
 
healthcheck = Namespace('healthcheck')

@healthcheck.route("/")
class HealthCheck(Resource):

    def get(self):  
        """    
        API health check
        """     
        response = make_response("the service is up")
        response.headers['Content-Type'] = "text/plain"
        return response