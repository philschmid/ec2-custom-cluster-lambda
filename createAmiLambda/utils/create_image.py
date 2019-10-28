import boto3 

def create_image(instance_id,name):
    ec2_client = boto3.client('ec2', region_name='eu-central-1')
    try:
        image = ec2_client.create_image(InstanceId=instance_id, NoReboot=True, Name=name)
        return image['ImageId']
    except:
        raise ValueError('couldn´t create ec2 Image')

