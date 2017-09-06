from flask import make_response
from flask import request
from flask_restplus import Namespace
from flask_restplus import Resource
from flask_restplus import fields
from flask_restplus import marshal

from v1.models import *
from v1.aws import *

endpoint = Namespace("elb")


model_machine_id = endpoint.model("MachineId", {
    "instanceId" : fields.String
})

model_machine_info = endpoint.model("MachineInfo", {
    "instanceId" : fields.String(attribute="instance_id"),
    "instanceType" : fields.String(attribute="instance_type"),
    "launchDate" : fields.String(attribute="launch_date")
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
        instances = get_elb_attached_instances(elb_name)
        if len(instances) == 0:
            return "", 404

        response = []
        for instance in instances:
            response.append(MachineInfo(instance_id = instance["instance_id"],
                                        instance_type = instance["instance_type"],
                                        launch_date = instance["launch_time"]))

        return marshal(response, model_machine_info), 200
        
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