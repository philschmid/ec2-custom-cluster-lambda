import boto3

def terminate_instance(instance_id):
    ec2 = boto3.resource('ec2', region_name='eu-central-1')
    try:
        instance = ec2.Instance(instance_id)
        instance.terminate()
        return True
    except:
        raise ValueError('couldn´t terminate ec2 instance')