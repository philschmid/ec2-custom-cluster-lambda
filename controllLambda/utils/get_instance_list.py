import boto3
ec2 = boto3.resource('ec2')

def get_instance_list(role):
    try:
        instances = list(ec2.instances.filter(Filters=[{'Name':'tag:module', 'Values':[role]},{'Name': 'instance-state-name', 'Values': ['running']}]))
        if(len(instances)<0):
            return[]
        return instances
    except:
        return []
#  for instance in instances:
#    print(instance.id, instance.instance_type)


# get_instance_list('translator')