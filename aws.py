import logging
from re import S
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
import uuid

# from filestorage import store

load_dotenv()

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
        image = f"https://{BUCKET}.s3.amazonaws.com/{object_name}"
    except ClientError as e:
        print('Image did not upload')
        logging.error(e)
        return False
    print('image', image, 'object_name', object_name)
    return [image, object_name]


def show_images(bucket=BUCKET):
    print("show_image")
    s3_client = boto3.client("s3")
    image_urls = []
    # print("s3_client", s3_client.list_objects(Bucket=BUCKET, Prefix=(FOLDER + "/")))
    try:
        for item in s3_client.list_objects(Bucket=BUCKET, Prefix=FOLDER)["Contents"]:
            presigned_url = s3_client.generate_presigned_url(
                "get_object", Params={"Bucket": BUCKET, "Key": item["Key"]}
            )
            image_urls.append(presigned_url)
        # print("image_urls", image_urls)
    except Exception as e:
        pass
    # print("[INFO] : The contents inside show_image = ", image_urls)
    return image_urls[1:]

show_images(BUCKET)
