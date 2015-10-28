import boto3
import logging
import psutil

logging.basicConfig(format='%(asctime)s %(message)s')

logging.warning('Checking alarm')

client = boto3.client('cloudwatch', region_name='us-east-1')
alarm = client.describe_alarms(AlarmNames=['noitemsinqueue'])

logging.warning('alarm is: %s', alarm)

if len(alarm['MetricAlarms']) > 0:
    logging.warning('we got something in metricalarms')
    if alarm['MetricAlarms'][0]['StateValue'] == 'ALARM':
        logging.warning('in alarm state, we should bail')

# now for java checking:
logging.warning('checking pids')
for p in psutil.process_iter():
    if p.name() == 'java':
        logging.warning('java is running!')
        exit(0)

logging.warning('java not running')

