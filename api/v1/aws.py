import boto3

def running_instances():
    ec2 = boto3.resource('ec2')

    instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        return "{} - {}".format(instance.id, instance.instance_type)

def get_elb_attached_instances(elb_name):
    elb_client = boto3.client('elb')

    elbs = elb_client.describe_load_balancers(LoadBalancerNames=[elb_name])
    elbs = elbs['LoadBalancerDescriptions'][0]

    print elbs['Instances']
    