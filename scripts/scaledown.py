import boto3
import logging
import psutil
import time
from subprocess import check_output


def java_is_running():
    logging.warning('checking if java is running')
    for p in psutil.process_iter():
        if p.name() == 'java':
            logging.warning('java is running')
            return True

    logging.warning('java not running')
    return False


def queue_empty_alarm_tripped():
    client = boto3.client('cloudwatch', region_name='us-east-1')
    alarms = client.describe_alarms(AlarmNames=['noitemsinqueue'])

    if len(alarms['MetricAlarms']) > 0:
        for alarm in alarms['MetricAlarms']:
            if alarm['AlarmName'] == 'noitemsinqueue':
                if alarm['StateValue'] == 'ALARM':
                    logging.warning('in alarm state for no messages in queue')
                    return True

    return False


def main():
    logging.basicConfig(format='%(asctime)s %(message)s')

    logging.warning('Checking if we should terminate ourselves')

    if java_is_running():
        exit(0)

    if queue_empty_alarm_tripped():
        # We're not running a job right now and the queue has been empty long enough to trip alarm.
        # Terminate ourselves.

        logging.warning('Java not running on this instance and queue empty alarm tripped: terminating this instance.')

        instance_id = check_output(["/opt/aws/bin/ec2-metadata", "-i"]).replace('instance-id: ', '').replace('\n', '')
        logging.warning('We are instance id "%s"', instance_id)

        client = boto3.client('autoscaling', region_name='us-east-1')
        client.terminate_instance_in_auto_scaling_group(
            InstanceId=instance_id,
            ShouldDecrementDesiredCapacity=True
        )

        # the above call will cause this script to abort if we're already at minimum instances.
        logging.warning('We want to shut down, sent the command, waiting 600s in scaledown.py')
        time.sleep(600)


if __name__ == "__main__":
    main()
