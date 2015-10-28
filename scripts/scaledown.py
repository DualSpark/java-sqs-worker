import boto3
import time
import logging
from subprocess import check_output


def java_is_running():
    # We'll need to actually check here, of course
    client = boto3.client('cloudwatch')
    
    return True


def queue_empty_alarm_tripped():
    # Actually check cloudwatch
    return False


def main():
    logging.basicConfig(format='%(asctime)s %(message)s')

    logging.warning('Checking if we should terminate ourselves')

    if java_is_running():
        exit(0)

    if queue_empty_alarm_tripped():
        # We're not running a job right now and the queue has been empty long enough to trip alarm.
        # Terminate ourselves.
        instance_id = check_output(["ec2-metadata", "-i"]).replace('instance-id: ', '')

        logging.warning('We are instance id %s', instance_id)

        client = boto3.client('autoscaling')

        response = client.terminate_instance_in_auto_scaling_group(
            InstanceId=instance_id,
            ShouldDecrementDesiredCapacity=True
        )

        # and we should be shutting down soon.


if __name__ == "__main__":
    main()
