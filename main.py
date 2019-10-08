from os.path import join, dirname
from dotenv import load_dotenv
 
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


def loadEnv():
    """ 
    Loads the enviroment vars like access key info
    to the file 
  
    Parameters: 
    None

    Returns: 
    None
    """
    # Create .env file path.
    dotenv_path = join(dirname(__file__), '.env')
    # Load file from the path.
    load_dotenv(dotenv_path)
    return

loadEnv()

def main():
    loadEnv()
    # boto3 client to get S3 data
    # Accessing variables.
    access_key_id = os.getenv('ACCESS_KEY_ID')
    secret_key = os.getenv('SECRET_KEY')    
    s3_client = boto3.client('s3',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_key)
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

main()