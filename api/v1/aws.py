import boto3
from botocore.exceptions import ClientError

def describe_instances(instance_ids):
    """
    Return informations about a list of instances
    :param instance_ids: List of instance ids
    """
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_instances(InstanceIds=instance_ids)
    instances = map(lambda reservation: reservation["Instances"][0], response["Reservations"])
    
    instance_info = []
    for instance in instances:
        instance_info.append({"instance_id" : instance["InstanceId"],
                              "instance_type" : instance["InstanceType"],
                              "launch_time" : instance["LaunchTime"],
                              "image_id" : instance["ImageId"],
                              "state" : instance["State"]
                            })
        
    return instance_info   


def get_elb_attached_instances(elb_name):
    """
    Return all instances attached to the load balancer
    :param elb_name: Loadb balancer name    
    """
    try:
        elb_client = boto3.client('elb')
        elbs = elb_client.describe_load_balancers(LoadBalancerNames=[elb_name])
        elbs = elbs['LoadBalancerDescriptions'][0]
        instance_ids = map(lambda instance_info: instance_info["InstanceId"], elbs['Instances'])
        return describe_instances(instance_ids)
    except ClientError:
        return []  