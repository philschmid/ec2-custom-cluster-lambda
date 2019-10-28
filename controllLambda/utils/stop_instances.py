import boto3

def stop_instances(instance_list,count):
    ec2 = boto3.resource('ec2', region_name='eu-central-1')
    print(count)
    print(instance_list[0].instance_id)
    try:
        for i in range(len(instance_list)-1, len(instance_list)-count-1, -1):
            print(i)
            instance = ec2.Instance(instance_list[i].instance_id).stop()
        return True
    except:
        raise 
    



# stop_instances([{'id': '123', 'instance_type':'test'},{'id': '1234', 'instance_type':'test'},{'id': '1235', 'instance_type':'test'}],2)