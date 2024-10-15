import boto3
import time


awsAccessKeyID = input("AWS Access Key: ")
awsSecretAccessKey = input("AWS Secret Access Key: ")


s3 = boto3.client(
    's3',
    aws_access_key_id=awsAccessKeyID,
    aws_secret_access_key=awsSecretAccessKey,
    region_name='eu-central-1'
)


response = s3.list_buckets()

if 'Buckets' in response and len(response['Buckets']) > 0:
    print("Current Buckets:")
    for bucket in response['Buckets']:
        print(f" - {bucket['Name']}")
else:
    print("No buckets found")


#----------------Upload Function
def upload_file_to_s3(file_name, bucket, object_name=None):
    try:
        if object_name is None:
            object_name = file_name
        
        s3.upload_file(file_name, bucket, object_name)
        print(f"{file_name} added to the bucket {bucket} successfully")
    
    except Exception as e:
        print(f"Error: {str(e)}")


#--------------List objects function
def list_objects_in_bucket(bucket_name):
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            print(f"Objects in {bucket_name}:")
            for obj in response['Contents']:
                print(f" - {obj['Key']}")
        else:
            print(f"No objects found in bucket {bucket_name}")
    except Exception as e:
        print(f"Error: {str(e)}")



#------------Download Function
def download_file_from_s3(bucket, object_name, local_path):
    try:
        s3.download_file(bucket, object_name, local_path)
        print(f"{object_name} downloaded from bucket {bucket} and saved to {local_path}")
    
    except Exception as e:
        print(f"Error: {str(e)}")



#------------Start
while True:
    operationNumber = None
    while operationNumber not in ['1', '2', 'q']:  
        operationNumber = input("Choose an operation (Type 1, 2 or q to quit):\n(1) Upload File\n(2) Download File\n(q) Quit\n")

    if operationNumber == '1':
        print("Upload File")
        time.sleep(0.5)

        bucket = input("Bucket name: ")
        file_name = input("File path which will be uploaded: ")
        object_name = input("File name which will appear in bucket: ")

        upload_file_to_s3(file_name, bucket, object_name)

    elif operationNumber == '2':
        print("Download File")
        time.sleep(0.5)

        bucket = input("Bucket name: ")
        list_objects_in_bucket(bucket)  
        
        object_name = input("Which file do you want to download (type the exact file name)? ")
        local_path = input("Path where you want to download the file: ") + "\\" +object_name

        download_file_from_s3(bucket, object_name, local_path)
    
    elif operationNumber == 'q':
        print("Exiting the program...")
        break  