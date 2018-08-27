import boto3
import botocore


ssm = boto3.client('ssm')


def get_ssm_client(endpoint_url=None):
    """ Returns an s3 session"""
    kwargs = {}
    if endpoint_url:
        kwargs['endpoint_url'] = endpoint_url
    ssm = boto3.client('ssm', region_name='us-east-1', **kwargs)
    return ssm


def put_parameter(key, value, Type='String', Description=''):
    ssm = get_ssm_client()
    resp = ssm.put_parameter(
         Name=key,
         Description=Description,
         Value=value,
         Type=Type,
         Overwrite=True
    )


def get_parameter(key, none_if_not_exists=False):
    ssm = get_ssm_client()
    try:
        resp = ssm.get_parameter(
            Name=key,
        )
        return resp['Parameter']['Value']
    except Exception as error:
        if (error.response['Error']['Code'] == 'ParameterNotFound'
           and none_if_not_exists):
            return None
        raise error
