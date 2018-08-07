import boto3
import urllib
from exceptions import NoEventRecordsException
from .s3 import get_object as get_s3_object
try:
    import simplejson as json
except ImportError:
    import json

def get_objects_from_event(event):
    if not event.has_key('Records') or not event['Records']:
        raise NoEventRecordsException(repr(event))
    for obj in event['Records']:
        if 's3' in obj:
            yield get_s3_object(obj['s3']['bucket']['name'], urllib.unquote(obj['s3']['object']['key']))
        if 'Sns' in obj:
            for obj2 in get_objects_from_event(json.loads(obj['Sns']['Message'])):
                yield obj2
