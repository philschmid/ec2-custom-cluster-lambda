# Infos

AMI.ecs-optimized: ami-084ab95c0cbe247e5

IAM Role in ec2 https://docs.aws.amazon.com/de_de/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html
set Credentials in docker https://cameroneckelberry.co/words/getting-aws-credentials-into-a-docker-container-without-hardcoding-it

# Requirements

1. process which can automate generating AMIs based on git pushes for CI/CD
2. AMIs which has model + start script when launching
3. lambda which can read the newest AMI-ID
4. lambda which can run 0-100 ec2 and scale down to 100-0
   3.a CF-Template which creates
   _ IAM Role for ec2 execution
   _ SecurityGroup for ec2 instance \* Subnet for ec2 instance

5. lambda which also monitors if something is wrong

## 1. Process which can automate generating AMIs

Create AMI with Cloudformation https://medium.com/poka-techblog/managing-amis-using-cloudformation-a097f86a3622
https://github.com/PokaInc/cloudformation-ami

write custom lambda for creating aws ami images

1. create ec2 instance

2. run instance with user_data
3. stop instance
4. create ami

```
ec2.create_image(InstanceId=instance_id, NoReboot=True, Name="abc")
```

5. terminate instance
6. create CF Stack with AMI-ID

## 2. lambda which can read the newest AMI-ID

Idea is to create AMI with CDK or cloudformation and output AMI-ID, in Lambda just reading this and starting the instances. So its dynamic and everytime the newest.
Maybe add some ENV var to override the output for using custom AMI-ID

## 3. Lambda which can start and stop ec2 instances

### Stopping based on InstanceID

```python
ec2.instances.filter(InstanceIds=ids).terminate()
```

### Starting new Images

#### easy start

```python
ec2.create_instances(ImageId='<ami-image-id>', MinCount=1, MaxCount=5)
```

#### start with without subnet

```python
import boto3

ec2 = boto3.resource('ec2')

user_data = '''#!/bin/bash
docker run xx'''

instance = ec2.create_instances(ImageId='ami-abcd1234', MinCount=1, MaxCount=1,
KeyName='my-key', SecurityGroupIds=['sg-abcd1234'], UserData=user_data,
InstanceType='t2.nano',
IamInstanceProfile={
'Name': 'ExampleInstanceProfile'
})
```

#### complete parameter with subnet

min Parameter for starting ec2 instance

- user data = start execution script
- run python3 app.py

```python
import boto3

ec2 = boto3.resource('ec2')

user_data = '''#!/bin/bash
echo 'test' > /tmp/hello'''

instance = ec2.create_instances(ImageId='ami-abcd1234', MinCount=1, MaxCount=1,
KeyName='my-key', SecurityGroupIds=['sg-abcd1234'], UserData=user_data,
InstanceType='t2.nano', SubnetId='subnet-abcd1234',
IamInstanceProfile={
'Arn': 'arn:aws:iam::123456789012:instanceprofile/ExampleInstanceProfile'
'Name': 'ExampleInstanceProfile'
})
```

#### Required Parameter/Ressources

- securitygroup
- subnet
- vpc

## 4. Lambda monitoring which ec2 is running

```python
 instances = ec2.instances.filter(
   Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
 for instance in instances:
   print(instance.id, instance.instance_type)
```

gets back instance.id for starting and stoping ec2 instances

### Using filters so get specific ec2 instances

```python
 filters = [{'Name':'tag:environment', 'Values':[Env]},
          {'Name':'tag:role', 'Values':[Role]}
         ]
 instances = ec2.instances.filter(
   Filters=filters)
```

# Links

- automating things with python3 https://stackabuse.com/automating-aws-ec2-management-with-python-and-boto3/
- boto3 for ec2 https://boto3.amazonaws.com/v1/documentation/api/latest/guide/migrationec2.html
- ec2 user data start script https://stackoverflow.com/questions/44190556/ec2-user-data-not-working-via-python-boto-command
- tool to build amis https://github.com/mickep76/docker-build-ami https://pypi.org/project/docker-build-ami/
- Create AMI with Cloudformation https://medium.com/poka-techblog/managing-amis-using-cloudformation-a097f86a3622 https://github.com/PokaInc/cloudformation-ami/blob/master/README.md#installation
