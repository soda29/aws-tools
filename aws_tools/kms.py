import boto3
import base64

botosess = boto3.session.Session()


def get_kms_client(endpoint_url=None):
    """ Returns an kms session"""
    kwargs = {}
    if endpoint_url:
        kwargs['endpoint_url'] = endpoint_url
    kms = botosess.client('kms', 'us-east-1', **kwargs)
    return kms


def get_kms_resource(endpoint_url=None):
    kwargs = {}
    if endpoint_url:
        kwargs['endpoint_url'] = endpoint_url
    kms = botosess.resource('kms', 'us-east-1', **kwargs)
    return s3


def decrypt(encrypted):
    '''Decrypt'''

    kms = get_kms_client()
    b64str = base64.b64decode(encrypted)
    decrypted = kms.decrypt(CiphertextBlob=b64str)['Plaintext']
    return decrypted

