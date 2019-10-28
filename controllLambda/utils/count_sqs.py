
import boto3

client = boto3.client('sqs',region_name='eu-central-1')

def count_sqs(queue_url):
    try:
        count = client.get_queue_attributes(QueueUrl=queue_url,AttributeNames=['ApproximateNumberOfMessages'])
        return count['Attributes']['ApproximateNumberOfMessages']
    except:
        raise ValueError("SQS didn't return ApproximateNumberOfMessages")


