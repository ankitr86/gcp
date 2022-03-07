import os
from google.cloud import bigquery

def csv_loader(data, context):
        client = bigquery.Client()
        dataset_id = os.environ['DATASET']
        dataset_ref = client.dataset(dataset_id)
        job_config = bigquery.LoadJobConfig()
        job_config.schema = [
                bigquery.SchemaField('id', 'INTEGER'),
                bigquery.SchemaField('first_name', 'STRING'),
                bigquery.SchemaField('last_name', 'STRING'),
                bigquery.SchemaField('email', 'STRING'),
                bigquery.SchemaField('gender', 'STRING'),
                bigquery.SchemaField('ip_address', 'STRING')
                ]
        job_config.skip_leading_rows = 1
        job_config.source_format = bigquery.SourceFormat.CSV

        # get the URI for uploaded CSV in GCS from 'data'
        uri = 'gs://' + os.environ['BUCKET'] + '/' + data['name']

        # lets do this
        load_job = client.load_table_from_uri(
                uri,
                dataset_ref.table(os.environ['TABLE']),
                job_config=job_config)

        print('Starting job {}'.format(load_job.job_id))
        print('Function=csv_loader, Version=' + os.environ['VERSION'])
        print('File: {}'.format(data['name']))

        load_job.result()  # wait for table load to complete.
        print('Job finished.')

        destination_table = client.get_table(dataset_ref.table(os.environ['TABLE']))
        print('Loaded {} rows.'.format(destination_table.num_rows))
