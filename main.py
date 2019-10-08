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

from sklearn.preprocessing import MinMaxScaler

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

def get_cleaned_data(data_body):
    """ 
    cleans the data by removing all the incomplete
    rows from the dataset 
  
    Parameters: 
    arg1 : bytes
    
    Returns: 
    dataFrame
    """
    # read in bytes data
    data_stream = io.BytesIO(data_body)

    # create a dataframe
    counties_df = pd.read_csv(data_stream, header=0, delimiter=",") 
    
    # print out stats about data
    old_shape = counties_df.shape
    print(old_shape)

    # drop any incomplete rows of data, and create a new df
    clean_counties_df = counties_df.dropna(axis=0)
    clean_counties_df.head()
    new_shape = clean_counties_df.shape
    print(new_shape)
    return clean_counties_df

def plot_histograms(clean_counties_df, list_of_features,n_bins):
    for column_name in list_of_features:
        ax=plt.subplots(figsize=(6,3))
        # get data by column_name and display a histogram
        ax = plt.hist(clean_counties_df[column_name], bins=n_bins)
        title="Histogram of " + column_name
        plt.title(title, fontsize=12)
        plt.show()
    return

def scaling_data_0_1(clean_counties_df):
    # scale numerical features into a normalized range, 0-1
    data_scaler=MinMaxScaler()
    # store them in this dataframe
    counties_scaled=pd.DataFrame(data_scaler.fit_transform(clean_counties_df.astype(float)))

    # get same features and State-County indices
    counties_scaled.columns=clean_counties_df.columns
    counties_scaled.index=clean_counties_df.index
    counties_scaled.head()
    return counties_scaled

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
    clean_counties_df = get_cleaned_data(data_body)

    # index data by 'State-County'
    clean_counties_df.index=clean_counties_df['State'] + "-" + clean_counties_df['County']

    # drop the old State and County columns, and the CensusId column
    clean_counties_df= clean_counties_df.drop(["State", "County", "CensusId"], axis=1)

    '''check histogram to find any valuble information before
        further preprocess to get insights on dataset
    '''
    #transportation (to work)
    #transport_list = ['Drive', 'Carpool', 'Transit', 'Walk', 'OtherTransp']
    #n_bins = 30 # can decrease to get a wider bin (or vice versa)
    #plot_histograms(clean_counties_df, transport_list, n_bins)

    counties_scaled = scaling_data_0_1(clean_counties_df)
    return

main()