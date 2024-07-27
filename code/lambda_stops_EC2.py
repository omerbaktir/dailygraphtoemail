import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='your-region')  # Specify your region
    instances = ['instance-id']  # Specify your instance ID
    ec2.stop_instances(InstanceIds=instances)
    return {
        'message': "EC2 instance stopped"
    }