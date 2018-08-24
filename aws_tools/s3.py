import boto3
from os import environ


botosess = boto3.session.Session()


def get_s3_client(endpoint_url=None):
    """ Returns an s3 session"""
    kwargs = {}
    if endpoint_url:
        kwargs['endpoint_url'] = endpoint_url
    s3 = botosess.client('s3', 'us-east-1', **kwargs)
    return s3


def get_s3_resource(endpoint_url=None):
    kwargs = {}
    if endpoint_url:
        kwargs['endpoint_url'] = endpoint_url
    s3 = botosess.resource('s3', 'us-east-1', **kwargs)
    return s3


def upload_file(bucket, key, data, public=False):
    '''Upload object file to S3'''
    s3 = get_s3_client()

    try:
        if public:
            s3.upload_fileobj(data, bucket, key,
                              ExtraArgs={'ACL': 'public-read'})
        else:
            s3.upload_fileobj(data, bucket, key)
        return 'https://s3.amazonaws.com/{}/{}'.format(bucket, key)
    except Exception as err:
        return 'Error: {}'.format(err)


def download_file(bucket, key, date):
    '''download data to s3'''
    s3 = get_s3_client()
    s3.download_file(bucket, key, '/tmp/id-{}.txt'.format(date))


def get_object(bucket, key):
    s3 = get_s3_resource()
    return s3.Object(bucket_name=bucket, key=key)
