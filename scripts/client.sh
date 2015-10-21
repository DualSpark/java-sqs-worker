#!/bin/sh

echo "Script to send files to S3 and work definitions to SQS."

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
echo "Would send job-input.zip to s3://javasqsworker12345/$timestamp/job-input.zip"
#aws s3 cp job-input.zip s3://javasqsworker12345/$timestamp/job-input.zip

# Send work message to SQS: needs bucket name, folder name to use.
# Server will assume job-input.zip is in bucket/foldername.
echo '{"bucket":"javasqsworker12345", "folder":"'$timestamp'"}'


# clean up:
rm job-input.zip



# upload constraints to S3
#echo "Uploading parameters file $2 to S3..."
#aws s3 cp $2 s3://javasqsworker12345/

# sed inline job definition: replace CONSTRAINTSLOCATION with the location we got back from S3 above
#cat $1 | sed -e "s/CONSTRAINTSLOCATION/s3:\/\/javasqsworker12345\/$2/" > ready-job.json

# Send message to SQS: https://sqs.us-east-1.amazonaws.com/347452556413/javasqsworker
#echo "Sending job description based off $1 to SQS..."
#aws sqs send-message --region us-east-1 --queue-url https://sqs.us-east-1.amazonaws.com/347452556413/javasqsworker \
#--message-body file://ready-job.json

# clean up our temp file
#echo "Cleaning up..."
#rm ready-job.json
