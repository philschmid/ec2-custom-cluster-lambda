import boto3
import time
ec2 = boto3.resource('ec2')

def create_ec2_tags(instances,role):
    time.sleep(1)
    for instance in instances:
        ec2.create_tags(Resources=[instance.id], Tags=[{'Key':'module', 'Value':role}])
    return True


