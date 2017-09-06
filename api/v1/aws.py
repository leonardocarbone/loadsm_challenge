import boto3

def running_instances():
    ec2 = boto3.resource('ec2')

    instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        return "{} - {}".format(instance.id, instance.instance_type)