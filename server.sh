#!/bin/sh

echo "File to pull work and data from SQS and S3."

# Fetch an SQS message (Defaults to reading a single message)
aws sqs receive-message --region us-east-1 --wait-time-seconds 10 \
--queue-url https://sqs.us-east-1.amazonaws.com/347452556413/javasqsworker > sqs-message.json

# Get the S3 location of the file

# Acquire file from S3
aws s3 cp FILELOCATION ./constraints.json

# Run the java jar on the job file and constraints
java -jar javasqsworker-1.0-SNAPSHOT.jar sqs-message.json constraints.json

# Once done, upload output to bucket
aws s3 cp output.zip OUTPUTS3BUCKET/job-name.zip

# clean up
rm sqs-message.json output.zip