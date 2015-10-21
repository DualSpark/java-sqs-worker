import boto3
import json
from subprocess import call

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

# Save message body (job description) to disk:
# Save to job.json

# delete message
# disabled for debug/dev purposes
#sqs_client.delete_message(QueueUrl=queue.url,ReceiptHandle=message.receipt_handle)

# get where to download things from S3
constraints_location = body['constraints_location']
print("constraints_location from body: ", constraints_location)

# download from S3
# Temp hardcoding, later on we'll extract from constraints_location
s3_client.download_file('javasqsworker12345', 'sample-constraints-1.json', 'constraints.json')

# run program
call(["java", "-jar javasqsworker-1.0-SNAPSHOT.jar job.json constraints.json"])

# upload results to S3
#s3_client.Bucket('javasqsworker12345').upload_file('output.zip', 'output.zip')

# Clean up job, constraints and output files.