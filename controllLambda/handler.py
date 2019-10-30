import boto3
import os
from utils.count_sqs import count_sqs
from utils.evaluate_scale import evaluate_scale
from utils.start_instance import start_instance
from utils.stop_instances import stop_instances
from utils.get_cf_outputs import get_cf_outputs
from utils.create_ec2_tags import create_ec2_tags
from utils.get_instance_list import get_instance_list
from utils.create_user_data import create_user_data
from utils.calculate_instance_number import calculate_instance_number


from dotenv import load_dotenv
load_dotenv()

client = boto3.client('ecs', region_name='eu-central-1')



# set Var for functionality -> get CF output stack (AMI-ID, SQS_QUEUE, S3_bucket)
# get messages in queue
# evalute ec2 instances (atm message_count / 5 )
# check how many instances are running, based on filter (module)
# calculate required instance ( +2 means -> has to start to more, -2 means stop 2 )
# if less instances are running start instances
# 6.1 start instance
# a. set min & max count to difference of actual running instances and evaluted_number
# b. wait until running
# c. set tag for instance (module)
# 6.2 if more instances are running stop instances
# a. get all instances and filter based on tags
# b. stop difference from actual running instances and evaluted_number
# finish

def ec2_scaler(event,context):
    instance={}
    try:
        # #
        #! # get cf output values
        # #
        # instance['image_id'] = get_cf_outputs(f"insight-translator-create-ami-{os.environ['STAGE']}","AMI-ID")
        instance['image_id'] = 'ami-0a93c6eb514c485e6'

        instance['security_group'] = get_cf_outputs('ec2-custom-cluster',f"security-group-name-{os.environ['SERVICENAME']}-{os.environ['STAGE']}")
        instance['instance_profile'] = get_cf_outputs('ec2-custom-cluster',f"instance-profile-name-{os.environ['SERVICENAME']}-{os.environ['STAGE']}")
        instance['iam_role'] = get_cf_outputs('ec2-custom-cluster',f"iam-role-name-{os.environ['SERVICENAME']}-{os.environ['STAGE']}")
        # #
        #! # create start script
        # #

        user_data_start = create_user_data(instance['iam_role'])
        print(user_data_start)

        # #
        #! # count messages in QUEUE
        # #
        try:
            # message_number = count_sqs(os.environ['sqs_queue_url'])
            message_number = 0
            # message_number = count_sqs(queue_url)
        except ValueError:
            return False
        print('message_number'+ str(message_number))

        #
        #! if no messages in Queue set desired_count to 0
        #
        if(message_number == 0):
            desired_count = 0
        else:
        #
        #! evaluates scale for message_number and sets desired_count
        #
            try:
                desired_count = evaluate_scale(message_number)
            except ValueError:
                print('error')
        print('desired_count'+str(desired_count))
        #         return False
        ##
        #!# get running instances
        ## 
        instance['running_instances'] = get_instance_list('translator')
        print("instance['running_instances']" + str(len(instance['running_instances'])))
        print(instance['running_instances'])
        # #
        #! # calculate instance number
        # # 
        instance_number = calculate_instance_number(evaluate_number=desired_count,instance_number=len(instance['running_instances']))
        print('instance_number'+str(instance_number))

        ## 
        #!# start/stop instance
        ##
        if(instance_number > 0):
            # start_instance(user_data=user_data_start,image_id=instance['image_id'],security_group=os.environ['security_group'],count=instance_number,instance_type=os.environ['instance_type'],iam_profil=os.environ['iam_profil'])
            started_instances_list=start_instance(user_data=user_data_start,image_id=instance['image_id'],security_group=instance['security_group'],count=instance_number,instance_type='t2.micro',iam_profil=instance['instance_profile'] )
            print(started_instances_list)
            create_ec2_tags(started_instances_list,'translator')
        elif(instance_number < 0 ):
            stop_instances(instance_list=instance['running_instances'],count=abs(instance_number))
        else:
            pass

    except Exception as e:
        print(e)


ec2_scaler('','')