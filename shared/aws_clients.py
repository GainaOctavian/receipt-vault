import os
import boto3

# Where the endpoint comes from: local (LocalStack) or empty (real AWS)
AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL")
AWS_REGION = os.getenv("AWS_REGION", "eu-central-1")


def _client(service_name: str):
    """Build a boto3 client for an AWS service.

    If AWS_ENDPOINT_URL is set, the client talks to LocalStack.
    If not, it talks to real AWS. The code stays exactly the same.
    """
    return boto3.client(
        service_name,
        endpoint_url=AWS_ENDPOINT_URL,  # None => boto3 goes to real AWS
        region_name=AWS_REGION,
    )


def s3_client():
    return _client("s3")


def sqs_client():
    return _client("sqs")