import boto3
ec2 = boto3.resource('ec2')

def start_instance(user_data,image_id,security_group,count,instance_type,subnet_id,iam_profil):
    try:
        # instance = ec2.create_instances(ImageId=image_id, MinCount=count, MaxCount=count,SecurityGroupIds=[security_group],SubnetId=subnet_id,KeyName='ec-2test', UserData=user_data, InstanceType=instance_type,IamInstanceProfile={'Name': iam_profil})
        instance = ec2.create_instances(ImageId=image_id, MinCount=count, MaxCount=count,KeyName='ec-2test', UserData=user_data, InstanceType=instance_type)
    except:
        raise 
    return True