import boto3
import botocore

ssm = boto3.client('ssm')

def put_parameter(key, value, Type='String', Description=''):
    resp = ssm.put_parameter(
         Name=key,
         Description=Description,
         Value=value,
         Type=Type,
         Overwrite=True
    )

def get_parameter(key, none_if_not_exists):
    try:
        resp = ssm.get_parameter(
            Name=key,
        )
        return resp['Parameter']['Value']
    except Exception as error:
        if error.response['Error']['Code'] == 'ParameterNotFound' and none_if_not_exists:
            return None
        raise error