"""
Original code contributor: mentzera
Article link: https://aws.amazon.com/blogs/big-data/building-a-near-real-time-discovery-platform-with-aws/
"""

import boto3
import json

# import twitter_to_es

# aws lambda update-function-code --function-name faucovidstream --zip-file fileb://lambda_s3_to_dynamo_and_kinesis.zip --region us-east-2
# from Examples.Demo.AWS_Related.TwitterStreamWithAWS.LambdaWithS3Trigger import \
#     twitter_to_es

from tweet_utils import get_reddit_data, reddit_id_field, get_tweet_mapping

headers = {"content-type": "application/json"}

s3 = boto3.client("s3")
kinesis_client = boto3.client("kinesis")
dynamodb_client = boto3.resource("dynamodb")
table = dynamodb_client.Table("faucovidstream_reddit_with_sentiment")

# {
#     "id_str": "1353185440401129478",
#     "hashtags": [],
#     "coordinates": None,
#     "timestamp_ms": "1611459524618",
#     "text": "RT @mas1z1: “once COVID is over” is starting to sound a lot like “he'll change😩😩😩\"",
#     "user": {"id": 1283078286382444544, "name": "Valentina 🦋"},
#     "mentions": ["@mas1z1"],
#     "emoticons": [],
#     "sentiments": 0.2,
# }


def convert_to_dynamodb_format(tw, platform):
    # tw["user"] = json.loads(tw["user"])
    # tw["platform"] = "twitter"
    tw.update(platform)
    return tw


# Lambda execution starts here
def handler(event, context):
    for record in event["Records"]:
        # print(record)
        # print("xxxxxxxxxxxxxxxxxxxxxxxxxx")

        # Get the bucket name and key for the new file
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        # Get s3 object, read, and split the file into lines
        try:
            obj = s3.get_object(Bucket=bucket, Key=key)

        except Exception as e:
            print(e)
            print(
                "Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.".format(
                    key, bucket
                )
            )
            raise e

            # Parse s3 object content (JSON)
        try:
            # https://stackoverflow.com/questions/31976273/open-s3-object-as-a-string-with-boto3
            s3_file_content = obj["Body"].read().decode("utf-8")

            # clean trailing comma
            if s3_file_content.endswith(",\n"):
                s3_file_content = s3_file_content[:-2]
            all_reddit_data_str = "[" + s3_file_content + "]"
            # print(tweets_str)
            all_reddit_data = json.loads(all_reddit_data_str)

        except Exception as e:
            print(e)
            print("Error loading json from object {} in bucket {}".format(key, bucket))
            raise e

        for doc in all_reddit_data:
            reddit_data = get_reddit_data(doc)  
            # reddit_data = get_tweet(doc)
            print(reddit_data["sentiments"])
            # =====================
            # ==kinesis
            # =====================
            timestamp_ms = str(reddit_data["timestamp_ms"])
            response = kinesis_client.put_record(
                StreamName="faucovidstreamsentiment_reddit",
                Data=json.dumps(reddit_data),
                PartitionKey=timestamp_ms,
            )

            print(type(reddit_data))
            print(reddit_data)

            # print([(i, type(j)) for i, j in tweet.items()])
            # tweet["user"] = json.dumps(tweet["user"])
            # print([(i, type(j)) for i, j in tweet.items()])

            # table.put_item(Item={"platform": "test", "timestamp_ms": "1607966429357"})

            table.put_item(
                Item=convert_to_dynamodb_format(reddit_data, {"platform": "reddit"})
            )
            print("===\n\n\n")

