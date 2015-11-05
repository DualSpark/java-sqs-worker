#!/bin/sh

# Set S3 bucket name here:
s3bucket="javasqsworker12345"

# we should be passed a job id
if [ "$#" -ne 1 ]; then
    echo "Please call in this format: cancel-job.sh job-to-cancel"
    exit -1
fi

touch $1

aws s3 cp $1 s3://$s3bucket/cancellations/

rm $1

echo "Sent cancellation request for job $1"
