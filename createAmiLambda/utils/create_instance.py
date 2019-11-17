import boto3 


def create_instance(user_data,iam_profil):
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
            #cpu
            #ImageId='ami-084ab95c0cbe247e5',
            #gpu 
            ImageId='ami-01dcb736f2bffd5bc',
            InstanceType='t2.micro',
            MaxCount=1,
            MinCount=1,
            UserData=user_data,
            IamInstanceProfile={'Name': iam_profil},
            KeyName='philipp-ec2-cluster'
        )
        return instance[0].instance_id
    except Exception as e: 
        print(e)    
        raise(e)
