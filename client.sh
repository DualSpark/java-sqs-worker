#!/bin/sh

echo "Script to send files to S3 and work definitions to SQS."

# we should be passed a job definition and a constraints/variable file, in that order
if [ "$#" -ne 2 ]; then
    echo "Please call in this format: client.sh job-definition.json variables.json"
    exit -1
fi

# upload constraints to S3
echo "Uploading constraints file to S3..."
aws s3 cp $2 s3://javasqsworker12345/

# sed inline job definition: replace CONSTRAINTSLOCATION with the location we got back from S3 above
cat $1 | sed -e "s/CONSTRAINTSLOCATION/s3:\/\/javasqsworker12345\/$2/" > ready-job.json

# Send message to SQS: https://sqs.us-east-1.amazonaws.com/347452556413/javasqsworker
echo "Sending job description to SQS..."
aws sqs send-message --region us-east-1 --queue-url https://sqs.us-east-1.amazonaws.com/347452556413/javasqsworker \
--message-body file://ready-job.json

# clean up our temp file
echo "Cleaning up..."
rm ready-job.json