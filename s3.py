import logging
from re import S
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
import os
from dotenv import load_dotenv
import uuid

# from filestorage import store

load_dotenv()


# Replace with your info
DO_SPACES_KEY = os.environ["DO_ACCESS_KEY"]
DO_SPACES_SECRET = os.environ["DO_SECRET_KEY"]
DO_REGION = os.environ["DO_REGION"]  # or sgp1, fra1, etc.
DO_ENDPOINT = f"https://{DO_REGION}.digitaloceanspaces.com"

session = boto3.session.Session()

s3 = session.client(
    's3',
    region_name=DO_REGION,
    endpoint_url=DO_ENDPOINT,
    aws_access_key_id=DO_SPACES_KEY,
    aws_secret_access_key=DO_SPACES_SECRET,
    config=Config(signature_version='s3v4')
)


BUCKET = os.environ["BUCKET"]
FOLDER = os.environ["FOLDER"]
print("bucket name", BUCKET)


def upload_file(file_name, bucket=BUCKET, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = f"{FOLDER}/"+str(uuid.uuid4())

    s3_client = boto3.client("s3")

    try:
        response = s3_client.upload_file(
            file_name,
            BUCKET,
            object_name,
            # ContentType="image/jpeg",
            # ACL='public-read'
        )

        print('response', response)
        image = f"https://{BUCKET}sfo2.digitaloceanspaces.com/{object_name}"
    except ClientError as e:
        print('Image did not upload')
        logging.error(e)
        return False
    print('image', image, 'object_name', object_name)
    return [image, object_name]


def get_images(bucket=BUCKET):

    s3_client = boto3.client("s3")
    image_urls = []
    try:
        for item in s3_client.list_objects(Bucket=BUCKET, Prefix=FOLDER)["Contents"]:
            presigned_url = s3_client.generate_presigned_url(
                "get_object", Params={"Bucket": BUCKET, "Key": item["Key"]}
            )
            image_urls.append(presigned_url)
    except Exception as e:
        print(f"errors: {e}")
        logging.error(e)
    return image_urls[1:]

get_images(BUCKET)
