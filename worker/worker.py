import os
import json
import time

from shared.aws_clients import s3_client, sqs_client
from shared.db import get_connection

BUCKET = os.getenv("S3_BUCKET", "receipts")
QUEUE_NAME = os.getenv("SQS_QUEUE", "receipts-to-process")

s3 = s3_client()
sqs = sqs_client()

queue_url = sqs.get_queue_url(QueueName=QUEUE_NAME)["QueueUrl"]


def extract_fields(file_bytes: bytes) -> dict:
    """Placeholder extraction. For now we return mock values.

    Later this becomes real parsing (regex) or AWS Textract.
    """
    return {
        "vendor": "Unknown Vendor",
        "amount": 0.00,
        "receipt_date": None,
    }


def save_metadata(s3_key: str, fields: dict):
    """Step 5: write the extracted metadata into Postgres."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO receipts (s3_key, vendor, amount, receipt_date) "
            "VALUES (%s, %s, %s, %s)",
            (s3_key, fields["vendor"], fields["amount"], fields["receipt_date"]),
        )
        conn.commit()


def process_message(message):
    body = json.loads(message["Body"])
    s3_key = body["s3_key"]

    # Step 4: read the file back from S3
    obj = s3.get_object(Bucket=BUCKET, Key=s3_key)
    file_bytes = obj["Body"].read()

    fields = extract_fields(file_bytes)
    save_metadata(s3_key, fields)
    print(f"Processed {s3_key}: {fields}")


def main():
    print("Worker started, polling for messages...")
    while True:
        # Long-poll the queue (waits up to 20s for a message)
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=5,
            WaitTimeSeconds=20,
        )
        messages = response.get("Messages", [])

        for message in messages:
            try:
                process_message(message)
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message["ReceiptHandle"],
                )
            except Exception as e:
                print(f"Failed to process message: {e}")

        if not messages:
            time.sleep(1)


if __name__ == "__main__":
    main()