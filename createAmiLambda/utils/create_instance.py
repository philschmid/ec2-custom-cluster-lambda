import boto3 


def create_instance(user_data):
    ec2 = boto3.resource('ec2', region_name='eu-central-1')
    try:
        instance = ec2.create_instances(
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/sdh',
                    'VirtualName': 'ephemeral0',
                    'Ebs': {
                        'DeleteOnTermination': True,
                        'VolumeSize': 10,
                        'VolumeType': 'gp2',
                        'Encrypted': False,
                    },
                },
            ],
            ImageId='ami-084ab95c0cbe247e5',
            InstanceType='t2.micro',
            MaxCount=1,
            MinCount=1,
            UserData=user_data,
        )
        return instance[0].instance_id
    except:
        raise ValueError('couldn´t start ec2 instance')