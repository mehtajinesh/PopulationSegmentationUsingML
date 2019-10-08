#import libs
import pandas as pd
import numpy as np
import os
import io
import matplotlib.pyplot as plt
import matplotlib
'exec(%matplotlib inline)'

# sagemaker libraries
import boto3
import sagemaker

# boto3 client to get S3 data
# TODO: need to move the keys to a env file for easier management
s3_client = boto3.client('s3',
         aws_access_key_id='AKIAIIIPE423XIAMEGVQ',
         aws_secret_access_key='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')
bucket_name='aws-ml-blog-sagemaker-census-segmentation'

# get a list of objects in the bucket
obj_list=s3_client.list_objects(Bucket=bucket_name)

# print object(s)in S3 bucket
files=[]
for contents in obj_list['Contents']:
    files.append(contents['Key'])
    
# there is one file --> one key
file_name=files[0]

# get an S3 object by passing in the bucket and file name
data_object = s3_client.get_object(Bucket=bucket_name, Key=file_name)

# information is in the "Body" of the object
data_body = data_object["Body"].read()
print('Data type: ', type(data_body))

# read in bytes data
data_stream = io.BytesIO(data_body)

# create a dataframe
counties_df = pd.read_csv(data_stream, header=0, delimiter=",") 
counties_df.head()