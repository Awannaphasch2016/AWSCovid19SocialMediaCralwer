import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr

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
        elif i == ":v4":
            args = event["ExpressionAttributeValues"][":v4"]["S"]

    if args == "":
        return {
            "statusCode": 400,
            "ErrorMessage": "please provide value for 'args' parameters",
        }
    else:
        try:
            args = int(args)
        except:
            return {
                "statusCode": 400,
                "ErrorMessage": "args paramater can't be converted to int",
            }

    dynamodb_client = init_dynamodb()
    table = dynamodb_client.Table(table_name)
    attr = boto3.dynamodb.conditions.Attr("timeStamp")
    # response = table.scan(FilterExpression=attr.between(since, until))

    if since == "" or until == "":
        if since != "":
            if aspect != "":
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
    items = items[: int(args)]

    return {
        "statusCode": 200,
        # "args": args,
        # "res": response,
        # "event": event,
        "count": len(items),
        "body": {"items": items},
    }
