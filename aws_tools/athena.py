import boto3
import time
from csv import reader
from . import s3
botosess = boto3.session.Session()
athena = botosess.client('athena')

AWS_ACCOUNT_ID = '094103223014'
output_location_path = 's3://aws-athena-query-results-{}-us-east-1'.format(AWS_ACCOUNT_ID)

def start_query_execution(query, database):
    response = athena.start_query_execution(
        QueryString=query,
        ResultConfiguration={
        'OutputLocation': output_location_path,
          'EncryptionConfiguration': {
            'EncryptionOption': 'SSE_S3'
          },
        },
        QueryExecutionContext={
            'Database': database
            },
        )
    print('Execution ID: ' + response['QueryExecutionId'])
    return response['QueryExecutionId']


def get_query_status(execution_id):
    response = athena.get_query_execution(
        QueryExecutionId=execution_id
    )
    status = response.get('QueryExecution')
    return status

def query(q, database):
    execution_id = start_query_execution(q, database)

    while get_query_status(execution_id).get('Status').get('State') == 'RUNNING':
        print 'sleeping...'
        time.sleep(10)

    status = get_query_status(execution_id)
    if status.get('Status').get('State') == 'SUCCEEDED':
        return {'bucket_name': output_location_path.lstrip('s3://'),
                'key': status['ResultConfiguration']['OutputLocation'].replace(
                    output_location_path, '').lstrip('/')}
    else:
        raise Exception(status)

def query_results(q, database, format_json=True):
    s3_params = query(q, database)
    result_object = s3.get_object(s3_params.get('bucket_name'), s3_params.get('key'))
    body = result_object.get()['Body']
    headers = []

    # iterating .csv athena result file row by row
    for n, line in enumerate(body._raw_stream):
        row = curate(line.strip())
        if format_json:
            if n == 0:
                headers = row
                continue
            yield dict(zip(headers, row))
        else:
            yield row

def curate(line):
    for l in reader([line]):
        return map(lambda x: None if not x else x, l)
