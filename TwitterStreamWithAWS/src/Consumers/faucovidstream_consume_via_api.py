import json
import os
import sys
from pprint import pprint
import requests

from TwitterStreamWithAWS.global_params import *

shard_id = json.loads(
    requests.get(API_STREAM + kinesiss_faucovidstreamsentiment + "/").text
)["StreamDescription"]["Shards"][0]["ShardId"]

shard_iterator = json.loads(
    requests.get(
        API_STREAM
        + kinesiss_faucovidstreamsentiment
        + "/"
        + f"sharditerator?shard-id={shard_id}"
    ).text
)["ShardIterator"]


def get_kinesis_stream_data(si):
    return json.loads(
        requests.get(
            API_STREAM + kinesiss_faucovidstreamsentiment + "/" + f"records",
            headers={"Shard-Iterator": si},
        ).text
    )


record_response = get_kinesis_stream_data(shard_iterator)

print("-----------------\n\n\n\n")

while "NextShardIterator" in record_response:

    # record_response = kinesis_client.get_records(
    #     ShardIterator=record_response["NextShardIterator"]
    # )
    record_response = get_kinesis_stream_data(record_response["NextShardIterator"])

    # Records', 'NextShardIterator', 'MillisBehindLatest', 'ResponseMetadata'
    # print(len(record_response["Records"]))
    # print(record_response["Records"][0]["Data"]["text"])

    try:
        print(record_response)

    except Exception as e:
        print(e)
        pass
