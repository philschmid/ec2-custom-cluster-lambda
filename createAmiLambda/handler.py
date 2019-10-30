# lambda for creating custom ami with docker image in it
import boto3 
from utils.create_instance import create_instance
from utils.create_image import create_image
from utils.stop_instance import stop_instance
from utils.terminate_instance import terminate_instance
from utils.wait_for_ec2 import wait_for_ec2
from utils.create_cloudformation import create_cloudformation
from utils.get_cf_outputs import get_cf_outputs

import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime

# user_data = '''#!/bin/bash
# sudo yum install python3 -y &&
# pip3 install awscli --upgrade --user &&
# sudo $(aws ecr get-login --region eu-central-1 --no-include-email);
# sudo docker pull 891511646143.dkr.ecr.eu-central-1.amazonaws.com/translator:latest &&
# pip3 uninstall awscli -y &&
# sudo yum remove python3 -y;
# ''' 

user_data = '''#!/bin/bash
docker pull philschmi/translator
''' 

def createAmi():
    instance={}
    ## creates instance
    instance['instance_profile'] = get_cf_outputs('ec2-custom-cluster',f"instance-profile-name-{os.environ['SERVICENAME']}-{os.environ['STAGE']}")

    instance['instance_id'] = create_instance(user_data=user_data,iam_profil= instance['instance_profile'])
    ## waiter for finishing user_data script
    wait_for_ec2(instance['instance_id'] )
    # stops instance 
    stop_instance(instance['instance_id'])
    ## create ami 
    instance['image_id'] = create_image(instance_id=instance['instance_id'],name=f"{os.environ['module']}-{datetime.today().strftime('%Y%m%d')}")
    ## termnaite ec2 instance 
    terminate_instance(instance['instance_id'])
    ## expose new ami_image_id
    print(instance['image_id'] )
    ## creates CF stack with Output
    create_cloudformation(image_id=instance['image_id'],cf_stack=f"{os.environ['stack_name']}-{os.environ['STAGE']}")
    return instance['image_id'] 

   
createAmi()



