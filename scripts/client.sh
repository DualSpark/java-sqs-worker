#!/bin/sh

echo "Script to send files to S3 and work definitions to SQS."

# Set S3 bucket name here:
s3bucket="javasqsworker12345"
# Set SQS URL here:
queueUrl="https://sqs.us-east-1.amazonaws.com/347452556413/asgtester"

# we should be passed a job definition and a constraints/variable file, in that order
if [ "$#" -ne 2 ]; then
    echo "Please call in this format: client.sh parameters-file input-file"
    exit -1
fi

# create a folder name to organize the job:
# once we have many people running jobs at once we'll need to add something like a userid (`whoami`) to this.
timestamp="$(date +"%s")"

# zip up parameters file and input file:
zip job-input.zip $1 $2

# upload job-input.zip to S3 under the timestamp dir:
# echo "Would send job-input.zip to s3://javasqsworker12345/$timestamp/job-input.zip"
aws s3 cp job-input.zip s3://$s3bucket/$timestamp/job-input.zip

# Send work message to SQS: needs bucket name, folder name to use.
# Server will assume job-input.zip is in bucket/foldername.

baseFile=$(basename $1)
# echo "baseFile is $baseFile"

# echo 'Would send this JSON in SQS message: {"bucket":"javasqsworker12345", "folder":"'$timestamp'"}'
echo '{"bucket":"'$s3bucket'", "folder":"'$timestamp'", "parameters":"'$baseFile'"}' > sqs-message.json

aws sqs send-message --region us-east-1 --queue-url $queueUrl --message-body file://sqs-message.json

# clean up:
rm job-input.zip sqs-message.json

echo "Job has been sent, results will be available at s3://$s3bucket/$timestamp/job-output.zip when finished."
echo "To download, run: \naws s3 cp s3://$s3bucket/$timestamp/job-output.zip ./\n"
echo "To see if the output file is present, run: \naws s3 ls s3://$s3bucket/$timestamp/"
