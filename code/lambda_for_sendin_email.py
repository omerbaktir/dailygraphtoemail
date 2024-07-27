import boto3
import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    ses_client = boto3.client('ses')

    # Extract bucket name and key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Get the file content from S3
    response = s3_client.get_object(Bucket=bucket_name, Key=key)
    file_content = response['Body'].read()

    # Create a MIME multipart message
    with open('emails.txt', 'r') as file:
        email_list = [line.strip() for line in file if line.strip()]

    msg = MIMEMultipart()
    msg['Subject'] = 'Daily Sales Graph'
    msg['From'] = 'your@email.net'
    msg['To'] = ', '.join(email_list)

    # Attach text body
    msg.attach(MIMEText('Here is the daily sales graph.', 'plain'))

    # Attach the image
    img = MIMEImage(file_content)
    img.add_header('Content-Disposition', 'attachment', filename=key)
    msg.attach(img)

    # Send the email
    try:
        response = ses_client.send_raw_email(
            Source=msg['From'],
            Destinations=email_list,  # Split the recipients into a list
            RawMessage={'Data': msg.as_string()}
        )
        print("Email sent! Message ID:", response['MessageId'])
    except ses_client.exceptions.MessageRejected as e:
        print("Email was rejected:", e)
    except ses_client.exceptions.MailFromDomainNotVerifiedException as e:
        print("Mail From domain not verified:", e)
    except Exception as e:
        print("Error sending email:", e)

    return {
        'statusCode': 200,
        'body': 'Email sent successfully!'
    }