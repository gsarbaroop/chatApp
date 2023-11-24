from google.cloud import storage
import os

os.environ["GCLOUD_PROJECT"] = "uplifted-woods-362215"

cred_path = "../../resources/application_default_credentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path


def list_blobs(bucket_name):
        storage_client = storage.Client()

        blobs = storage_client.list_blobs(bucket_name)

        for blob in blobs:
                print(blob.name)


def read(bucket_name, blob_name):
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        with blob.open("r") as f:
                print(f.read())

def write_read(bucket_name, file):
        name = file.split("/")[-1]
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        d = 'bucketz-for-webapp/' + name
        d = bucket.blob(d)
        with open(file, 'rb') as my_file:
                d.upload_from_file(my_file)

# write_read("bucketz-for-webapp", "../../resources/media/IMG-20230902-WA0008.jpg")
# list_blobs("bucketz-for-webapp")
read("bucketz-for-webapp","bucketz-for-webapp/IMG-20230902-WA0008.jpg")