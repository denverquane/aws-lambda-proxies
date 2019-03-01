import boto3
import json

REGION = 'us-west-1'  # region to launch instance.
AMI = 'ami-8d948ced'
# matching region/setup amazon linux ami, as per:
# https://aws.amazon.com/amazon-linux-ami/

EC2 = boto3.client('ec2', region_name=REGION)


def lambda_to_ec2(event, context):
    eventObj = json.loads(event['body'])
    print eventObj

    proxy_user = eventObj['PROXY_USER']
    proxy_pass = eventObj['PROXY_PASSWORD']
    proxy_port = eventObj['PROXY_PORT']
    proxy_type = eventObj['PROXY_TYPE']
    instance_type = eventObj['INSTANCE_TYPE']
    uniqueHash = eventObj["UNIQUE_ID"]

    response = EC2.create_security_group(GroupName='ec2_sg_' + uniqueHash,
                                         Description='Managed by Lambda')
    security_group_id = response['GroupId']
    print('Security Group Created %s' % (security_group_id))

    data = EC2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': int(proxy_port),
             'ToPort': int(proxy_port),
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])

    print('Ingress Successfully Set %s' % data)

    init_script = """#!/bin/bash
yum update -y
curl -L https://raw.githubusercontent.com/snail007/goproxy/master/install_auto.sh | sudo bash

if [ -n \"""" + proxy_user + """\" ] && [ -n \"""" + proxy_pass + """\" ]; then
  COMMAND=\"""" + proxy_type + """ -t tcp -p '0.0.0.0:""" + proxy_port + """' -a '""" + proxy_user + """:""" + proxy_pass + """'"
else
  COMMAND=\"""" + proxy_type + """ -t tcp -p '0.0.0.0:""" + proxy_port + """'"
fi

sudo echo "[Unit]
Description=Proxy server
Requires=network.target
[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu
ExecStart=/bin/bash -lc '/usr/bin/proxy ${COMMAND}'
TimeoutSec=15
Restart=always
[Install]
WantedBy=multi-user.target" > /etc/systemd/system/proxy.service

# Enable service
sudo systemctl daemon-reload
sudo systemctl enable proxy.service
sudo systemctl start proxy.service

# Print status
sudo systemctl status proxy.service --no-pager"""

    print 'Running script:'
    print init_script

    instance = EC2.run_instances(
        ImageId=AMI,
        InstanceType=instance_type,
        MinCount=1,  # required by boto, even though it's kinda obvious.
        MaxCount=1,
        # make shutdown in script terminate ec2
        InstanceInitiatedShutdownBehavior='terminate',
        UserData=init_script,  # file to run on instance init.
        SecurityGroupIds=[
            security_group_id
        ],
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'Proxy ' + uniqueHash
                }
            ]
        }]
    )

    print "New instance created."
    instance_id = instance['Instances'][0]['InstanceId']
    print instance_id

    return {
        "statusCode": 200,
        "body":
            "{ \"instance_id\": \"" + instance_id + "\"," +
            "\"sg_id\": \"" + security_group_id + "\"," +
            "\"type\": \"" + instance_type + "\"" +
            "}"
    }
