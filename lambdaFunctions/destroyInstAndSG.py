import boto3
import json

REGION = 'us-west-1' # region for instance termination

EC2 = boto3.client('ec2', region_name=REGION)

def lambda_handler(event, context):
    eventObj = json.loads(event['body'])
    print eventObj
    
    instance_id = eventObj['INSTANCE_ID']
    security_group_id = eventObj['SG_ID']
    
    print "Destroying instance " + instance_id
    
    print EC2.terminate_instances(
        InstanceIds = [
            instance_id
            ])
            
    destroyWaiter = EC2.get_waiter('instance_terminated')
    destroyWaiter.wait(
        InstanceIds=[
            instance_id
            ])
            
    print "Destroying Security Group: " + security_group_id
    
    print EC2.delete_security_group(
        GroupId=security_group_id
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }
