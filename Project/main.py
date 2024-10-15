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

#------------Delete Function
def delete_file_from_s3(bucket, object_name):
    try:
        s3.delete_object(Bucket=bucket, Key=object_name)
        print(f"Object {object_name} successfully deleted from bucket {bucket}.")
    
    except Exception as e:
        print(f"Error: {str(e)}")


#-------------Create Bucket
def create_s3_bucket(bucket_name):
    try:
        response = s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': 'eu-central-1'  
            }
        )
        print(f"Bucket '{bucket_name}' created successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")

#------------Start
while True:
    operationNumber = None
    while operationNumber not in ['1', '2', '3', '4', '5', 'q']:  
        operationNumber = input("Choose an operation (Type 1, 2, 3, 4, 5 or q to quit):\n(1) Upload File\n(2) Download File\n(3) Delete File\n(4) List objects in bucket\n(5) Create new bucket\n(q) Quit\n")

    if operationNumber == '1':
        print("Upload File")
        time.sleep(0.5)

        bucket = input("Bucket name: ")
        file_name = input("File path which will be uploaded: ")
        object_name = input("File name which will appear in bucket: ")

        upload_file_to_s3(file_name, bucket, object_name)
        time.sleep(3)

    elif operationNumber == '2':
        print("Download File")
        time.sleep(0.5)

        bucket = input("Bucket name: ")
        list_objects_in_bucket(bucket)  
        
        object_name = input("Which file do you want to download (type the exact file name)? ")
        local_path = input("Path where you want to download the file: ") + "\\" + object_name

        download_file_from_s3(bucket, object_name, local_path)
        time.sleep(3)
        

    elif operationNumber == '3':
        print("Delete File")
        time.sleep(0.5)
        
        bucket = input("Bucket name: ")
        list_objects_in_bucket(bucket)

        while True:
            object_name = input("Which file do you want to delete (type the exact file name)? ")

            confirm = input("Please write the file name again to confirm: ")
            if confirm == object_name:
                delete_file_from_s3(bucket, object_name)
                break
                time.sleep(3)

            else:
                print("You wrote wrong")
                time.sleep(0.5)


    elif operationNumber == '4':
        bucket = input("Bucket name:")
        list_objects_in_bucket(bucket)
        time.sleep(3)


    elif operationNumber == '5':
        bucket = input("Write the bucket name you want to create: ")
        create_s3_bucket(bucket)
        

    elif operationNumber == 'q':
        print("Exiting the program...")
        break  
