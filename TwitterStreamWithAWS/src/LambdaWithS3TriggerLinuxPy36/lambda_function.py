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

from tweet_utils import get_tweet, id_field, get_tweet_mapping

headers = {"Content-Type": "application/json"}

s3 = boto3.client("s3")
kinesis_client = boto3.client("kinesis")
dynamodb_client = boto3.resource("dynamodb")
table = dynamodb_client.Table("faucovidstream_twitter_with_sentiment")

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
            tweets_str = "[" + s3_file_content + "]"
            # print(tweets_str)
            tweets = json.loads(tweets_str)

        except Exception as e:
            print(e)
            print("Error loading json from object {} in bucket {}".format(key, bucket))
            raise e

        for doc in tweets:
            tweet = get_tweet(doc)
            print(tweet["sentiments"])
            # =====================
            # ==kinesis
            # =====================
            timestamp_ms = str(tweet["timestamp_ms"])
            response = kinesis_client.put_record(
                StreamName="faucovidstreamsentiment",
                Data=json.dumps(tweet),
                PartitionKey=timestamp_ms,
            )

            print(type(tweet))
            print(tweet)

            # print([(i, type(j)) for i, j in tweet.items()])
            # tweet["user"] = json.dumps(tweet["user"])
            # print([(i, type(j)) for i, j in tweet.items()])

            # table.put_item(Item={"platform": "test", "timestamp_ms": "1607966429357"})

            table.put_item(
                Item=convert_to_dynamodb_format(tweet, {"platform": "twitter"})
            )
            print("===\n\n\n")

        # # Load data into ES
        # try:
        #     twitter_to_es.load(tweets)
        # except Exception as e:
        #     print(e)
        #     print('Error loading data into ElasticSearch')
        #     raise e

        # #=====================
        # #==kinesis
        # #=====================
        #
        # timestamp_ms = tweets['timestamp_ms']
        # kinesis_input_data = json.dumbs(twitter)
        # kinesis_input_data = bytes(kinesis_input_data, 'utf-8')
        #
        # response = kinesis_client.put_record(
        #     StreamName='    faucovidstreamsentiment',
        #     Data=kinesis_input_data,
        #     PartitionKey=timestamp_ms,
        #     SequenceNumberForOrdering='string'
        # )

        # #=====================
        # #==dynamoDB
        # #=====================
        # dynamoDb_client.put_item()
