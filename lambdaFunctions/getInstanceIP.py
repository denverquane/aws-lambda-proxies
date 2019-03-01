import boto3
import json

REGION = 'us-west-1' # region the instance was launched in

EC2 = boto3.client('ec2', region_name=REGION)

def lambda_handler(event, context):
    eventObj = json.loads(event['body'])
    print eventObj
    
    instance_id = eventObj['INSTANCE_ID']
    
    # wait for the server to be running, just in case
    waiter = EC2.get_waiter('instance_running')
    waiter.wait(
        InstanceIds=[
            instance_id
        ]
    )
    
    # get the updated instance info when the server is running
    instance = EC2.describe_instances(
        InstanceIds=[
            instance_id
        ]
    )
        
    return {
        'statusCode': 200,
        'body': "{\"ip\": \"" + instance['Reservations'][0]['Instances'][0]['PublicIpAddress'] + "\"}"
    }
