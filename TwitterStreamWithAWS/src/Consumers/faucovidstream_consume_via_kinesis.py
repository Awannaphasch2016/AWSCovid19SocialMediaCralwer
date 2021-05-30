import ast
import json
import os
import time
from pprint import pprint

import boto3
# stream_name = "faucovidstreamsentiment"
# stream_name = "faucovidstreamsentiment_reddit"
stream_name = "faucovidstream-input"
kinesis_client = boto3.client(
    "kinesis",
    region_name="us-east-2",  # enter the region
    # aws_access_key_id="AKIA3ZMDQYM6TSTIV6GN",
    # aws_secret_access_key="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",
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)

# stream_name = 'transforminputtoS3'
# kinesis_client = boto3.client('firehose',
#                               region_name='us-east-2',  # enter the region
#                               aws_access_key_id='AKIAIET5BC65M6AQN23Q',
#                               # fill your AWS access key id
#                               aws_secret_access_key='sC4FP3Q61k43Lk9tks4TRyidSCk3H5PtdFbvEh7q')

response = kinesis_client.describe_stream(StreamName=stream_name)
shard_id = response["StreamDescription"]["Shards"][0]["ShardId"]

# shard_iterator = kinesis_client.get_shard_iterator(
#     StreamName=stream_name, ShardId=shard_id, ShardIteratorType="TRIM_HORIZON"
# )


shard_iterator = kinesis_client.get_shard_iterator(
    StreamName=stream_name, ShardId=shard_id, ShardIteratorType="LATEST"
)


# print(shard_iterator)

my_shard_iterator = shard_iterator["ShardIterator"]

# record_response = kinesis_client.get_records(ShardIterator=my_shard_iterator, Limit=2)
record_response = kinesis_client.get_records(ShardIterator=my_shard_iterator)
pprint(response)

# response = kinesis_client.get_records()

# response = kinesis_client.list_shards(
#     StreamName=stream_name,
#     MaxResults=123,
# )

# pprint(response)
def return_all_data_from_kinesis_record() -> int:
    for i in record_response["Records"]:
        # bytes_data = i["Data"]
        # yield json.loads("".join(map(chr, bytes_data)))["sentiments"]
        # print(bytes_data[:-2])
        # print(bytes_data)
        # print(json.loads(bytes_data[:-2])['sentiments'])
        print(json.loads(bytes_data[:-2]))
        # exit()
        # print(json.loads("".join(map(chr, bytes_data)))["sentiments"])


print("-----------------\n\n\n\n")
while "NextShardIterator" in record_response:
    record_response = kinesis_client.get_records(
        ShardIterator=record_response["NextShardIterator"]
    )
    # Records', 'NextShardIterator', 'MillisBehindLatest', 'ResponseMetadata'
    # print(len(record_response["Records"]))
    # print(record_response["Records"][0]["Data"]["text"])

    try:

        # print(record_response)
        # exit()

        # print(len(record_response["Records"]))
        # print(record_response["Records"])

        print("++++++++++++++")
        print(len(record_response["Records"]))
        bytes_data = record_response["Records"][0]["Data"]
        print("xxxxxxxxxxxxxxxxxx")
        print(return_all_data_from_kinesis_record())
        # while True:
        #     try:
        #         data = next(return_all_data_from_kinesis_record())
        #     except StopIteration:
        #         break
        #     print(data)
        # print(json.loads("".join(map(chr, bytes_data)))["sentiments"])
        # print(bytes_data)
        # print(json.loads("".join(map(chr, bytes_data[:-2])))
        # print(json.loads("".join(map(chr, bytes_data))).keys())
        # print(json.loads("".join(map(chr, bytes_data))))
        # bytes_to_str = lambda x: "".join(map(chr, x))
        # str_data = bytes_to_str(bytes_data)
        # print(str_data)
        print("======")
        # json_data = json.loads(str_data)
        # print(json_data)
        # # exit()

        # print(json_data["text"])
        # print(json_data["sentiment"])
        # print(json_data.keys())
        # exit()

    except Exception as e:
        print(e)
        pass

    # time.sleep(1)
