#To access storage client
from google.cloud import storage
#To access OS file system
import os
import hashlib
import time

#variable declaration
file_name = "src_employee.csv"
file_name_path = "D:/GCP/sourcecode/src_employee.csv"
source_filepath = r"D:/GCP/sourcecode/src_employee.csv"
assert os.path.isfile(source_filepath)
Bucket_name="aankietcsvbucket"
md5value = ""
newmsd5value = "0"
fileComplete="N"

md5_hash = hashlib.md5()

#To validate condition/existence of the file


#Authentication key file
key_file = r"D:/GCP/sourcecode/aankiet-myproject-day1-de835dfe534b.json"
assert os.path.isfile(key_file)

#Upload file function
def upload_file(file_name, source_filepath, Bucket_name):
    storage_client = storage.Client.from_service_account_json(key_file)
    bucket = storage_client.get_bucket(Bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_filename(source_filepath)
    print("\n\n** Upload File Function completed **")

def fileCompleteNess() :
    md5value = ""
    newmsd5value = "0"
    fileComplete="N"
    print ("\nStart of file check in process....")
    while md5value != newmsd5value :
        
        with open(file_name_path,"rb") as f:
            # Read and update hash in chunks of 4K
            for byte_block in iter(lambda: f.read(4096),b""):
                md5_hash.update(byte_block)
                md5value=md5_hash.hexdigest()
                newmsd5value=md5value
                print(md5value)
                time.sleep(12)
                fileComplete="N"
    print ("\nSource File is Complete File")

#Function call to check file upload is successfull            
fileCompleteNess()

fileComplete="Y"

#Function call to load file from local to GCP Bucket
upload_file(file_name, source_filepath, Bucket_name)
 




