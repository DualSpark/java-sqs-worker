import boto3
import json

# Get the service resource
sqs_service = boto3.resource('sqs', region_name='us-east-1')
sqs_client = boto3.client('sqs', region_name='us-east-1')
s3_client = boto3.client('s3', region_name='us-east-1')

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
constraints_location = body['constraints_location']
print("constraints_location from body: ", constraints_location)

# download from S3
s3.download_file("bucketname", "filename", "localfilename")

# run program

# upload results to S3
#s3.Bucket('mybucket').upload_file('/tmp/hello.txt', 'hello.txt')
