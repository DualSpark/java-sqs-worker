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
    alarm = client.describe_alarms(AlarmNames=['noitemsinqueue'])

    if len(alarm['MetricAlarms']) > 0:
        logging.warning('we got something in metricalarms')
        if alarm['MetricAlarms'][0]['StateValue'] == 'ALARM':
            logging.warning('in alarm state')
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

        # and we should be shutting down soon.  Stay here until we do:
        time.sleep(10000)


if __name__ == "__main__":
    main()
