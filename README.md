# Proof of concept for Java app pulling work from SQS

## Overview

The java application takes one argument: the work definition file.  It processes
it and outputs data.  Real applications would do actual computation with them.

## Server Python script

An included Python script uses the AWS SDK to poll SQS for messages and pull them one at a time to work it.
The SQS message includes the work definition file and the S3 location of the variables/constraints file that goes with it.

See [bmserver.py](scripts/bmserver.py).

## Server scripts

Included is an [upstart script](scripts/bmserver.conf) to treat the program as a service that
will automatically restart if needed.  

Copy files to the instance with SCP.  This would be replaced with letting [packer.io](http://packer.io)
doing the work automatically:

```bash
scp -i ~/.ssh/KEYPAIR.pem bmserver.conf ec2-user@IPADDRESS:~/
scp -i ~/.ssh/KEYPAIR.pem bmlogs.conf ec2-user@IPADDRESS:~/
scp -i ~/.ssh/KEYPAIR.pem bmserver.py ec2-user@IPADDRESS:~/
```

On the EC2 instance:

```bash
sudo yum install -y gcc
sudo pip install psutil
sudo pip install boto3
sudo cp bmserver.conf /etc/init/bmserver.conf
sudo start bmserver
sudo cp bmlogs.conf /etc/logrotate.d/bmserver
```


## Client shell script

A wrapper around the AWS CLI to upload the variables/constraints file to S3 and send an SQS message of a work file.

See [client.sh](scripts/client.sh).

### Cancelling a job

Cancellations can be signaled via the S3 bucket's "cancellations" folder.  Use [cancel-job.sh](scripts/cancel-job.sh)
to cancel a job.  The SQS message will still pick up the work to do but the instance performing
the work will cancel the job after a few minutes and move on to the next item of work.
