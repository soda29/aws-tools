import logging
import boto3
from email import encoders
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import mimetypes

logger = logging.getLogger(__name__)

def send_email(source, destination, message, **kwargs):
    '''Send email'''
    client = boto3.client('ses', 'us-east-1')
    result = client.send_email(Source=source,
         Destination=destination,
         Message=message,
         ReplyToAddresses=kwargs.get('reply_to') or [])
    if 'ErrorResponse' in result:
            logger.info("[Error] send email: {}".format(result))
    return result

def send_raw_email():
    pass

def send_email_with_attachment(source, destination, message, attachments):
    # The attachment
    msg = MIMEMultipart()
    msg['Subject'] = message['Subject']['Data']
    msg['From'] = source
    msg['To'] = ','.join(destination)
    if 'Html' in message['Body']:
        html = MIMEText(message['Body']['Html']['Data'], 'html')
        msg.attach(html)
    if 'Text' in message['Body']:
        text = MIMEText(message['Body']['Text']['Data'], 'text')
        msg.attach(text)
    for attach in attachments:
        part = MIMEApplication(attach['data'])
        mime = mimetypes.guess_type(attach['filename'])[0]
        # print mime
        part.add_header('Content-Disposition', 'attachment', filename=attach['filename'])
        part.add_header('Content-Type', mime)
        msg.attach(part)

    client = boto3.client('ses', 'us-east-1')
    client.send_raw_email(
        Source=source,
        Destinations=destination,
        RawMessage={
            'Data': msg.as_string(),
        }
    )
