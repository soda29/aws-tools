import boto3
import base64

def decrypt(encrypted):
    '''Decrypt'''
    decrypted = boto3.client('kms').decrypt(CiphertextBlob=base64.b64decode(
        encrypted))['Plaintext']
    return decrypted
