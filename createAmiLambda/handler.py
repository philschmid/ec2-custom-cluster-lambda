# lambda for creating custom ami with docker image in it
import boto3 
from utils.create_instance import create_instance
from utils.create_image import create_image
from utils.stop_instance import stop_instance
from utils.terminate_instance import terminate_instance
from utils.wait_for_ec2 import wait_for_ec2
from utils.create_cloudformation import create_cloudformation

user_data = '''#!/bin/bash
docker pull hello-world'''

def handler():
    instance={}
    ## creates instance
    instance['instance_id'] = create_instance(user_data=user_data)
    ## waiter for finishing user_data script
    wait_for_ec2(instance['instance_id'] )
    ## stops instance 
    stop_instance(instance['instance_id'])
    ## create ami 
    instance['image_id'] = create_image(instance_id=instance['instance_id'],name="test")
    ## termnaite ec2 instance 
    terminate_instance(instance['instance_id'])
    ## expose new ami_image_id
    print(instance['image_id'] )
    ## creates CF stack with Output
    create_cloudformation(image_id=instance['image_id'],cf_stack='AMI-Creation')
    return instance['image_id'] 

   
handler()