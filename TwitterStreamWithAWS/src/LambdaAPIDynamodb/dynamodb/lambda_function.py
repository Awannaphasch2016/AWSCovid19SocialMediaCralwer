import json
from datetime import datetime

import boto3
from boto3.dynamodb.conditions import Attr, Key

# import requests


def init_dynamodb():
    # create kinesis client connection
    return boto3.resource(
        "dynamodb",
        region_name="us-east-2",  # enter the region
        # aws_access_key_id="AKIAIET5BC65M6AQN23Q",
        # # fill your AWS access key id
        # aws_secret_access_key="sC4FP3Q61k43Lk9tks4TRyidSCk3H5PtdFbvEh7q",
    )  # fill you aws secret access key


# def lambda_handler(event, context):
#     return {"statuscode": 200}


def get_all_data_using_paginator():
    # client = boto3.client(
    #     service_name,
    #     region_name="us-east-2",  # enter the region
    # )  # fill you aws secret access key
    # # paginatoy = client.get_paginator("scan")
    # paginator = client.get_paginator("query")

    res = boto3.resource("dynamodb")
    paginator = res.meta.client.get_paginator("query")

    for page in paginator.paginate(
        TableName=table_name,
        # FilterExpression=Key("platform").begins_with("twitter"),
        # FilterExpression=Key("platform").eq("twitter"),
        # FilterExpression="platform = twitter",
        # Select="COUNT",
        # FilterExpression="begins_with(platform, twitter)",
        ScanIndexForward=False,
        KeyConditionExpression=Key("platform").eq("twitter"),
        # KeyConditionExpression="platform = twitter",
        # PaginationConfig={"PageSize": 1, "MaxItems": 5000, "MaxSize": 1},
        # PaginationConfig={"PageSize": 2, "MaxItems": 5},
    ):

        # dict_keys(['Items', 'Count', 'ScannedCount', 'LastEvaluatedKey', 'ResponseMetadata'])
        print(page["Count"])
        print(page["ScannedCount"])
        print(convert_to_datetime(int(page["LastEvaluatedKey"]["timestamp_ms"])))
        # print(page["ResponseMetadata"])

        # items = page["Items"]
        # print(page.keys())
        # print(page)
        # print(items)
        # print(len(items))
        # print(items)
        # print(items[0]["timestamp_ms"])
        # print(convert_to_datetime(int(items[0]["timestamp_ms"])))

        # print(items)
        print("====")


def lambda_handler(event, context):
    """
    'since' and 'until' can't be used for query because I mistakenly set 'timestamp_ms' sort key to be string.
     'timestamp_ms' should be converted to int so that it can be used to compare against 'since' and 'until'
        To solve this issue, I need to create new dynamodb that haave the same key and value except
         'timestamp_ms' sort key mst have int type
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e
    since = ""
    until = ""
    aspect = ""
    args = ""

    print(event)

    table_name = event["TableName"]
    attrs = event["ExpressionAttributeValues"]

    for i in attrs.keys():
        platform = event["ExpressionAttributeValues"][":v1"]["S"]
        if i == ":v2a":
            since = event["ExpressionAttributeValues"][":v2a"]["S"]
        elif i == ":v2b":
            until = event["ExpressionAttributeValues"][":v2b"]["S"]
        elif i == ":v3":
            aspect = event["ExpressionAttributeValues"][":v3"]["S"]

    dynamodb_client = init_dynamodb()
    table = dynamodb_client.Table(table_name)
    paginator = res.meta.client.get_paginator("query")

    attr = boto3.dynamodb.conditions.Attr("timeStamp")
    # response = table.scan(FilterExpression=attr.between(since, until))

    if since == "" or until == "":
        if since != "":
            if aspect != "":
                # response = paginator
                response = table.query(
                    KeyConditionExpression=Key("platform").eq(platform)
                    & Key("timestamp_ms").gte(since),
                    FilterExpression=Attr("text").contains(aspect),
                )
            else:
                response = table.query(
                    KeyConditionExpression=Key("platform").eq(platform)
                    & Key("timestamp_ms").gte(since)
                )
        elif until != "":
            if aspect != "":
                response = table.query(
                    KeyConditionExpression=Key("platform").eq(platform)
                    & Key("timestamp_ms").lte(until),
                    FilterExpression=Attr("text").contains(aspect),
                )
            else:
                response = table.query(
                    KeyConditionExpression=Key("platform").eq(platform)
                    & Key("timestamp_ms").lte(until)
                )
        else:
            if aspect != "":
                response = table.query(
                    KeyConditionExpression=Key("platform").eq(platform),
                    FilterExpression=Attr("text").contains(aspect),
                )
            else:
                response = table.query(
                    KeyConditionExpression=Key("platform").eq(platform)
                )
    else:
        if aspect != "":
            response = table.query(
                KeyConditionExpression=Key("platform").eq(platform),
                # & Key("timestamp_ms").between(since, until),
                # & Key("timestamp_ms").lte(until)
                # & Key("timestamp_ms").gte(since),
                FilterExpression=Attr("text").contains(aspect),
            )
        else:
            response = table.query(
                KeyConditionExpression=Key("platform").eq(platform)
                # & Key("timestamp_ms").between(since, until),
                # & Key("timestamp_ms").lte(until)
                # & Key("timestamp_ms").gte(since)
            )

    # response = response["items"][: args]
    items = response["Items"]

    # return {
    #     "statusCode": 200,
    #     # "args": args,
    #     # "res": response,
    #     # "event": event,
    #     "count": len(items),
    #     "body": {"items": items},
    # }

    return {
        "statusCode": 200,
        # "args": args,
        # "res": response,
        # "event": event,
        "count": len(items),
        "body": {"items": items},
    }

# get_all_data_using_paginator()

