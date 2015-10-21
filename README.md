# Proof of concept for Java app pulling work from SQS

## Overview

The java application takes one argument: the work definition file and the variables/constraints files.  It processes
those and outputs data.  Real applications would do actual computation with them.

## Server Python script

An included Python script uses the AWS SDK to poll SQS for messages and pull them one at a time to work it.
The SQS message includes the work definition file and the S3 location of the variables/constraints file that goes with it.

See [server.py](server.py).

## Client shell script

A wrapper around the AWS CLI to upload the variables/constraints file to S3 and send an SQS message of a work file.

See [client.sh](client.sh).