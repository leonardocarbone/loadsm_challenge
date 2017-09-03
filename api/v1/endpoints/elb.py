from flask import make_response
from flask_restplus import Namespace
from flask_restplus import Resource
from flask_restplus import fields


endpoint = Namespace("elb")

@endpoint.route("/<elb_name>")
@endpoint.doc(params={"elb_name" : "pass the load balancer name"})
class Elb(Resource):

    @endpoint.response(200, "machines listed")
    @endpoint.response(404, "the elb does not exist")
    def get(self, elb_name):  
        """    
        List machines attached to a particular load balancer
        """   
        # Return 404 when the elb does not exist  
        response = make_response("", 404)
        response.headers['Content-Type'] = "text/plain"
        return response

    @endpoint.doc(body={"machineId" : "instance identifier"})
    @endpoint.response(201, "instance added")  
    @endpoint.response(400, "wrong data format")
    @endpoint.response(409, "instance already on load balancer")
    def post(self, elb_name, instance_id):
        """
        Attach an instance on the load balancer
        """
        print "CARALHO {}".format(elb_name)