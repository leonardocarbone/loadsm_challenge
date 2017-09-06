from flask import make_response
from flask import request
from flask_restplus import Namespace
from flask_restplus import Resource
from flask_restplus import fields

from v1.models import MachineId
from v1.aws import running_instances

endpoint = Namespace("elb")


model_machine_id = endpoint.model("MachineId", {
    "instanceId" : fields.String
})

model_machine_info = endpoint.model("MachineInfo", {
    "instanceId" : fields.String,
    "instanceType" : fields.String,
    "launchDate" : fields.String
})


@endpoint.route("/<elb_name>")
@endpoint.doc(params={"elb_name" : "pass the load balancer name"})
class Elb(Resource):

    @endpoint.response(200, "machines listed")
    @endpoint.response(404, "the elb does not exist")
    def get(self, elb_name):  
        """    
        List machines attached to a particular load balancer
        """   
        instances = running_instances()
        # Return 404 when the elb does not exist  
        response = make_response(instances, 404)
        response.headers['Content-Type'] = "text/plain"
        return response


    @endpoint.expect(model_machine_id, validate=True)    
    @endpoint.response(201, "instance added")  
    @endpoint.response(400, "wrong data format")
    @endpoint.response(409, "instance already on load balancer")
    def post(self, elb_name):
        """
        Attach an instance on the load balancer
        """
        data = request.json
        machine = MachineId()
        machine.instance_id = data["instanceId"]
        print "CARALHO {}".format(machine.instance_id)
        return "ok", 201

    @endpoint.expect(model_machine_id, validate=True)    
    @endpoint.response(201, "instance removed")  
    @endpoint.response(400, "wrong data format")
    @endpoint.response(409, "instance is not on load balancer")
    def delete(self, elb_name):
        """
        Detach an instance from the load balancer
        """