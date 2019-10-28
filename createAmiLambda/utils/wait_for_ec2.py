import boto3


def wait_for_ec2(instance_id):
    ec2_client = boto3.client('ec2', region_name='eu-central-1')
    try:
        waiter = ec2_client.get_waiter('instance_status_ok')
        waiter.wait(InstanceIds=[instance_id])
        return True
    except:
        raise ValueError('couldn´t wait for ec2 instance')