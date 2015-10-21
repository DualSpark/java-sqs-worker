import boto3
import json
from subprocess import call

# Get the service resource
sqs_service = boto3.resource('sqs', region_name='us-east-1')
sqs_client = boto3.client('sqs', region_name='us-east-1')
s3_client = boto3.client('s3', region_name='us-east-1')

# Get the queue. This returns an SQS.Queue instance
queue = sqs_service.get_queue_by_name(QueueName='javasqsworker')

# TODO: loop around the remainder of the file, forever!

# Grab the first messsage
message_list = queue.receive_messages(MaxNumberOfMessages=1, WaitTimeSeconds=5)

# TODO: don't assume we received a message
if len(message_list) == 0:
    print("Didn't get a message, waiting and trying again...")
    exit(1) # TODO: continue in infinite loop

message = message_list[0]

# delete message
sqs_client.delete_message(QueueUrl=queue.url,ReceiptHandle=message.receipt_handle)

body = json.loads(message.body)

# body has two fields: bucket and folder.  Extract those.
bucket = body['bucket']
folder = body['folder']

call(["mkdir", "temp-work"])

object_location = folder + '/job-input.zip'
print('downloading object at ' + object_location)

# download job-input.zip:
s3_client.download_file(bucket, object_location, 'temp-work/job-input.zip')

# unzip job-input
call(["unzip", "temp-work/job-input.zip", "-d", "temp-work/"])

# run bidmaster on job-input
print("Would have called the java process here")
# pretending we have results from bidmaster:
f = open('temp-work/logfile.log', 'w')
f.write('logs')
f.close()
f = open('temp-work/stdout.log', 'w')
f.write('stdout')
f.close()
f = open('temp-work/results.txt', 'w')
f.write('results')
f.close()


# call(["java", "-jar javasqsworker-1.0-SNAPSHOT.jar temp-work/job.json temp-work/constraints.json"])

# zip results, log file, stdout from bidmaster to job-output.zip
call(["zip", "temp-work/job-output.zip", "temp-work/logfile.log", "temp-work/stdout.log", "temp-work/results.txt"])

# upload results to bucket/folder/job-output.zip
s3_client.upload_file('temp-work/job-output.zip', bucket, folder + '/job-output.zip')

# Clean up job, constraints and output files.
# print("Would have deleted the temp-work folder here")
call(["rm", "-rf", "temp-work/"])
