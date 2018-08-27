import boto3
from urllib.parse import unquote
from aws_tools.exceptions import NoEventRecordsException
from aws_tools.s3 import get_object as get_s3_object

try:
    import simplejson as json
except ImportError:
    import json


def get_objects_from_event(event):
    if 'Records' not in event or event['Records'] is None:
        raise NoEventRecordsException(repr(event))
    for obj in event['Records']:
        if 's3' in obj:
            yield get_s3_object(obj['s3']['bucket']['name'],
                                unquote(obj['s3']['object']['key']))
        if 'Sns' in obj:
            for obj2 in get_objects_from_event(
                json.loads(obj['Sns']['Message'])
            ):
                yield obj2
