import os
import json
import uuid

from fastapi import FastAPI, UploadFile, HTTPException

from shared.aws_clients import s3_client, sqs_client
from shared.db import get_connection

BUCKET = os.getenv("S3_BUCKET", "receipts")
QUEUE_NAME = os.getenv("SQS_QUEUE", "receipts-to-process")

app = FastAPI(title="Receipt Vault")

s3 = s3_client()
sqs = sqs_client()

queue_url = sqs.get_queue_url(QueueName=QUEUE_NAME)["QueueUrl"]


@app.post("/receipts")
async def upload_receipt(file: UploadFile):
    """Step 1-2: store the file in S3, then enqueue a job to process it."""
    s3_key = f"{uuid.uuid4()}-{file.filename}"

    # Step 1: store the raw file in S3
    contents = await file.read()
    s3.put_object(Bucket=BUCKET, Key=s3_key, Body=contents)

    # Step 2: enqueue a small message pointing at the file
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps({"s3_key": s3_key}),
    )

    return {"status": "accepted", "s3_key": s3_key}


@app.get("/receipts")
def list_receipts():
    """Step 6: read processed metadata back from the database."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, vendor, amount, receipt_date, s3_key "
            "FROM receipts ORDER BY created_at DESC"
        ).fetchall()

    return [
        {
            "id": r[0],
            "vendor": r[1],
            "amount": float(r[2]) if r[2] is not None else None,
            "date": str(r[3]) if r[3] else None,
            "s3_key": r[4],
        }
        for r in rows
    ]


@app.get("/totals")
def monthly_totals():
    """Monthly totals, grouped by month."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT to_char(receipt_date, 'YYYY-MM') AS month, "
            "SUM(amount) AS total FROM receipts "
            "WHERE receipt_date IS NOT NULL "
            "GROUP BY month ORDER BY month"
        ).fetchall()

    return [{"month": r[0], "total": float(r[1])} for r in rows]