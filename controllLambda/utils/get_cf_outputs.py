import boto3 


def get_cf_outputs(stack_name,export_name):
    cf_conn = boto3.client('cloudformation', region_name='eu-central-1')
    stack = cf_conn.describe_stacks(StackName=stack_name)
    # check with index you need couldn´t test it
    # print(stack['Stacks'][0]['Outputs'])
    return list(filter(lambda output: output['ExportName'] == export_name, stack['Stacks'][0]['Outputs']))[0]['OutputValue']


get_cf_outputs('ec2-custom-cluster','SUBNET-NAME')