import boto3
import json

from process import process_file

# Create SQS client
sqs = boto3.resource('sqs',
  endpoint_url=os.environ['SQS_ENDPOINT'],
  aws_access_key_id=os.environ['SQS_ID'],
  aws_secret_access_key=os.environ['SQS_SECRET'],
  region_name=os.environ['SQS_REGION'])

queue = sqs.Queue(url=os.environ['SQS_QUEUE_URL'])

messages = queue.receive_messages(
    MaxNumberOfMessages=1,
    WaitTimeSeconds=10,
)

print(f"Number of messages received: {len(messages)}")

for message in messages:
    content = json.loads(message.body)
    result = process_file(content['file_id'])
    message.delete()
