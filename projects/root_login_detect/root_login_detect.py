import json
import boto3

def lambda_handler(event, context):
    print(event)
    # Create SNS client
    sns_client = boto3.client('sns')
    
    # Extract root user login details from the CloudWatch event
    user_name = event['detail']['userIdentity'].get('userName', 'Unknown')
    login_status = event['detail']['responseElements'].get('ConsoleLogin', 'Failure')
    source_ip = event['detail'].get('sourceIPAddress', 'Unknown')
    event_time = event['detail'].get('eventTime', 'Unknown')
    
    # Create the notification message
    message = f"Root User Login Attempt:\n"
    message += f"User: {user_name}\n"
    message += f"Login Status: {login_status}\n"
    message += f"Source IP: {source_ip}\n"
    message += f"Event Time: {event_time}\n"

    # SNS Topic ARN (replace with your SNS topic ARN)
    sns_topic_arn = 'arn:aws:sns:us-east-1:851725172472:RootUserLoginNotifications'

    # Send the notification via SNS
    sns_response = sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=message,
        Subject="AWS Root User Login Notification"
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Notification sent successfully')
    }
