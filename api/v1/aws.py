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
    :param elb_name: Load balancer name
    """
    try:
        elb_client = boto3.client('elb')
        elbs = elb_client.describe_load_balancers(LoadBalancerNames=[elb_name])
        elbs = elbs['LoadBalancerDescriptions'][0]
        instance_ids = map(lambda instance_info: instance_info["InstanceId"], elbs['Instances'])
        return describe_instances(instance_ids)
    except ClientError:
        return []  


def add_elb_instance(elb_name, instance_ids):
    """
    Add instances to load balancer
    :param elb_name: Load balancer name
    :instance_ids: List of instance ids
    """
    instance_ids = map(lambda id: {"InstanceId":id}, instance_ids)

    elb_client = boto3.client("elb")
    response = elb_client.register_instances_with_load_balancer(LoadBalancerName=elb_name, Instances=instance_ids)
    attached_instances = map(lambda instance: instance["InstanceId"], response["Instances"])

    return attached_instances    


def remove_elb_instance(elb_name, instance_ids):
    """
    Remove instances from load balancer
    :param elb_name: Load balancer name
    :instance_ids: List of instance ids
    """
    instance_ids = map(lambda id: {"InstanceId":id}, instance_ids)

    elb_client = boto3.client("elb")
    response = elb_client.deregister_instances_from_load_balancer(LoadBalancerName=elb_name, Instances=instance_ids)
    remaining_ids  = map(lambda instance: instance["InstanceId"], response["Instances"])
    
    return remaining_ids


def is_instance_attached_to_elb(elb_name, instance_id):
    """
    Check if an instance is attached to ELB
    :param elb_name: Load balancer name
    :instance_id: Instance id
    """
    attached_instances = get_elb_attached_instances(elb_name)
    attached_instances = filter(lambda instance: instance["instance_id"] == instance_id, attached_instances)

    if len(attached_instances) == 1:
        return True
    else:
        return False