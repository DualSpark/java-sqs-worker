import boto3
import logging

logging.basicConfig(format='%(asctime)s %(message)s')

logging.warning('Checking alarm')

client = boto3.client('cloudwatch', region_name='us-east-1')
alarm = client.describe_alarms(AlarmNames=['noitemsinqueue'])

logging.warning('alarm is: %s', alarm)

if len(alarm['MetricAlarms']) > 0:
    logging.warning('we got something in metricalarms')
    if alarm['MetricAlarms'][0]['StateValue'] == 'ALARM':
        logging.warning('in alarm state, we should bail')