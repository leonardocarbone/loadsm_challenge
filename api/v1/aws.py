import boto3

def running_instances():
    ec2 = boto3.resource('ec2', region_name="us-east-2b")

    instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        print(instance.id, instance.instance_type)