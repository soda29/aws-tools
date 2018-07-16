import boto3
botosess = boto3.session.Session()

def upload_file(bucket, key, data, public=False):
    '''Upload object file to S3'''
    s3 = botosess.client('s3', 'us-east-1')
    try:
        if public:
            s3.upload_fileobj(
            data, bucket, key,
            ExtraArgs={'ACL': 'public-read'}
            )
        else:
            s3.upload_fileobj(data, bucket, key)
        return 'https://s3.amazonaws.com/{}/{}'.format(bucket, key)
    except Exception as err:
        return 'Error: {}'.format(err)

def download_file(bucket, key, date):
    '''download data to s3'''
    s3 = botosess.client('s3', 'us-east-1')
    s3.download_file(bucket, key, '/tmp/id-{}.txt'.format(date))

def get_object(bucket, key):
    s3 = botosess.resource('s3')
    return s3.Object(bucket_name=bucket, key=key)
