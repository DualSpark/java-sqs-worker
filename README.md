# Proof of concept for Java app pulling work from SQS

## Overview

The java application takes one argument: the work definition file.  It processes
it and outputs data.  Real applications would do actual computation with them.

## Server Python script

An included Python script uses the AWS SDK to poll SQS for messages and pull them one at a time to work it.
The SQS message includes the work definition file and the S3 location of the variables/constraints file that goes with it.

See [bmserver.py](scripts/bmserver.py).

## Server init.d script

Included is an [init.d script](scripts/bmserver) to treat the program as a service.  On the EC2 instance:

```bash
chmod +x bmserver
sudo cp bmserver /etc/init.d/bmserver
sudo chkconfig bmserver on
sudo service bmserver start
```

The init script will run the Python script on startup with the `chkconfig bmserver on` line and start it
manually immediately with the `service bmserver start` command.

## Client shell script

A wrapper around the AWS CLI to upload the variables/constraints file to S3 and send an SQS message of a work file.

See [client.sh](scripts/client.sh).
