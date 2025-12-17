from google.cloud import storage
import os

# Initialize the client
# If you've set up application default credentials, no need to specify credentials
client = storage.Client()

# Alternative: Specify credentials explicitly
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/service-account-key.json'
# client = storage.Client.from_service_account_json('path/to/service-account-key.json')

def list_buckets():
    """List all buckets in your GCP project"""
    buckets = client.list_buckets()
    print("Buckets in project:")
    for bucket in buckets:
        print(f"  - {bucket.name}")

def list_blobs(bucket_name):
    """List all files in a specific bucket"""
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs()
    print(f"\nFiles in bucket '{bucket_name}':")
    for blob in blobs:
        print(f"  - {blob.name}")

def upload_file(bucket_name, source_file_path, destination_blob_name):
    """Upload a file to GCS bucket"""
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)
    print(f"\nFile {source_file_path} uploaded to {destination_blob_name}")

def download_file(bucket_name, source_blob_name, destination_file_path):
    """Download a file from GCS bucket"""
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_path)
    print(f"\nFile {source_blob_name} downloaded to {destination_file_path}")

def read_file_content(bucket_name, blob_name):
    """Read file content directly without downloading"""
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    content = blob.download_as_text()
    print(f"\nContent of {blob_name}:")
    print(content)
    return content

def delete_file(bucket_name, blob_name):
    """Delete a file from GCS bucket"""
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()
    print(f"\nFile {blob_name} deleted from {bucket_name}")

# Example usage
if __name__ == "__main__":
    # List all buckets
    list_buckets()
    
    # Replace with your bucket name
    BUCKET_NAME = "mlops-project-1-rhic"
    
    # List files in a bucket
    # list_blobs(BUCKET_NAME)
    
    # Upload a file
    # upload_file(BUCKET_NAME, "local_file.txt", "remote_file.txt")
    
    # Download a file
    # download_file(BUCKET_NAME, "remote_file.txt", "downloaded_file.txt")
    
    # Read file content
    # read_file_content(BUCKET_NAME, "remote_file.txt")
    
    # Delete a file
    # delete_file(BUCKET_NAME, "remote_file.txt")