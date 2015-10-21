import boto3
import json

# Get the service resource
sqs_service = boto3.resource('sqs', region_name='us-east-1')
sqs_client = boto3.client('sqs', region_name='us-east-1')

# Get the queue. This returns an SQS.Queue instance
queue = sqs_service.get_queue_by_name(QueueName='javasqsworker')

# Grab the first messsage
message_list = queue.receive_messages(MaxNumberOfMessages=1, WaitTimeSeconds=5)
message = message_list[0]
body = json.loads(message.body)
#print("First message body: ", body)

# delete message
#sqs_client.delete_message(QueueUrl=queue.url,ReceiptHandle=message.receipt_handle)

# get where to download things from S3
print("constraints_location from body: ", body['constraints_location'])

# download from S3

# run program

# upload results to S3

