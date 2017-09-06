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

    def new_machine_info(self, instance_info):
        return MachineInfo(instance_id = instance_info["instance_id"],
                           instance_type = instance_info["instance_type"],
                           launch_date = instance_info["launch_time"])

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
            response.append(self.new_machine_info(instance))

        return marshal(response, model_machine_info), 200
        
    @endpoint.expect(model_machine_id, validate=True)    
    @endpoint.response(201, "instance added")  
    @endpoint.response(400, "wrong data format")
    @endpoint.response(409, "instance already on load balancer")
    def post(self, elb_name):
        """
        Attach an instance on the load balancer
        """
        try:
            instance_id = request.json["instanceId"]
        except:
            return "", 400

        if is_instance_attached_to_elb(elb_name, instance_id):
            return "", 409

        added_instance = add_elb_instance(elb_name, [instance_id])
        added_instance = self.new_machine_info(describe_instances([instance_id])[0])
        return marshal(added_instance, model_machine_info), 201

    @endpoint.expect(model_machine_id, validate=True)    
    @endpoint.response(201, "instance removed")  
    @endpoint.response(400, "wrong data format")
    @endpoint.response(409, "instance is not on load balancer")
    def delete(self, elb_name):
        """
        Detach an instance from the load balancer
        """
        try:
            instance_id = request.json["instanceId"]
        except:
            return "", 400

        if not is_instance_attached_to_elb(elb_name, instance_id):
            return "", 409
        
        remove_elb_instance(elb_name, [instance_id])
        removed_instance = self.new_machine_info(describe_instances([instance_id])[0])
        
        return marshal(removed_instance, model_machine_info), 201