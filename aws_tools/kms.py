import boto3
import base64

def decrypt(encrypted):
    '''Decrypt'''
    decrypted = boto3.client('kms', region_name='us-east-1').decrypt(CiphertextBlob=base64.b64decode(
        encrypted))['Plaintext']
    return decrypted
