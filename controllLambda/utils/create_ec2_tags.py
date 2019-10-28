import boto3
ec2 = boto3.resource('ec2')

def create_ec2_tags(instances,role):
    ec2.create_tags(Resources=[instances], Tags=[{'Key':'module', 'Value':role}])
    return True