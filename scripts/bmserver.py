import boto3
import psutil
import json
import time
import logging
import os
from subprocess import call, Popen
from botocore.exceptions import ClientError


# def pretend_java_call():
#     logging.warning("Would have called the java process here, faking outputs for testing")
#     # pretending we have results from bidmaster:
#     f = open('/home/ec2-user/temp-work/logfile.log', 'w')
#     f.write('logs')
#     f.close()
#     f = open('/home/ec2-user/temp-work/stdout.log', 'w')
#     f.write('stdout')
#     f.close()
#     f = open('/home/ec2-user/temp-work/results.txt', 'w')
#     f.write('results')
#     f.close()

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

def call_java(parameters_file, bucket, folder, s3_client):
    # chdir here
    # remove this once we don't need to simulate output files:
    # pretend_java_call()

    # This won't take down our Python script if it exits poorly:
    bidmaster_job = Popen(["java", "-jar", "./javasqsworker-1.0-SNAPSHOT.jar"])

    while bidmaster_job.poll() is None:
        logging.warning("Bidmaster job still running, no cancellation request, waiting 30s before checking again")
        time.sleep(30)

        try:
            s3_client.head_object(Bucket=bucket, Key="cancellations/" + folder)
            # Getting anything means the cancellation request is there.
            logging.warning('Found cancellation request, aborting Java run.')
            kill(bidmaster_job.pid)

        except ClientError as e:
            # May want to silently swallow exceptions instead of bloating logs:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                logging.warning('Didn\'t find a cancellation, continuing...')


    # We probably want to return this to mark the job as "something went wrong."
    logging.warning('bidmaster_job return code: %s', bidmaster_job.returncode)
    # chdir here

def main():
    logging.basicConfig(format='%(asctime)s %(message)s')

    # logging.warning('Starting up, waiting 120s for credentials to become available.')
    # time.sleep(120)

    # Get the service resource
    sqs_service = boto3.resource('sqs', region_name='us-east-1')
    sqs_client = boto3.client('sqs', region_name='us-east-1')
    s3_client = boto3.client('s3', region_name='us-east-1')

    # Get the queue. This returns an SQS.Queue instance
    queue = sqs_service.get_queue_by_name(QueueName='asgtester')

    # may want to make this step options for easier local testing:
    os.chdir('/home/ec2-user/')

    while True:
        logging.warning('Checking SQS for work to do.')

        # Grab the first messsage
        message_list = queue.receive_messages(MaxNumberOfMessages=1, WaitTimeSeconds=5)

        if len(message_list) == 0:
            logging.warning("Didn't get a message, seeing if we need to shut down.")
            # call scaledown.py: if it returns, keep going.
            # if it doesn't return it's because we're shutting down.
            call(["python", "/home/ec2-user/scaledown.py"])

            logging.warning('no need to shut down, polling SQS after sleeping 30s')
            time.sleep(30)
            continue

        message = message_list[0]

        sqs_client.delete_message(QueueUrl=queue.url, ReceiptHandle=message.receipt_handle)

        # body has three fields: bucket, folder, parameters file.  Extract those.
        body = json.loads(message.body)
        bucket = body['bucket']
        folder = body['folder']
        parameters_file = body['parameters']

        call(["mkdir", "-p", "/home/ec2-user/temp-work"])

        # download job-input.zip:
        input_file_location = folder + '/job-input.zip'
        s3_client.download_file(bucket, input_file_location, '/home/ec2-user/temp-work/job-input.zip')

        # unzip job-input
        call(["unzip", "-o", "/home/ec2-user/temp-work/job-input.zip", "-d", "/home/ec2-user/temp-work/"])

        # run bidmaster on job-input
        call_java("/home/ec2-user/temp-work/" + parameters_file, bucket, folder, s3_client)

        # zip results, log file, stdout from bidmaster to job-output.zip
        call(["zip", "-r", "/home/ec2-user/temp-work/job-output.zip", "/home/ec2-user/temp-work"])

        # upload results to bucket/folder/job-output.zip
        s3_client.upload_file('/home/ec2-user/temp-work/job-output.zip', bucket, folder + '/job-output.zip')

        # Clean up job, constraints and output files.
        call(["rm", "-rf", "/home/ec2-user/temp-work/"])

        logging.warning("Done with the job, checking to see if we should terminate ourselves.")


if __name__ == "__main__":
    main()
