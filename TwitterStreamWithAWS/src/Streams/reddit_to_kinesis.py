import datetime
import inspect
import json
import os
import sqlite3
from pprint import pprint
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

# LOGGER = MyLogger()
# PROGRAM_LOGGER = LOGGER.program_logger
import boto3
import praw

# from TwitterStreamWithAWS.credentials import REDDIT_CLIENT_ID
# from TwitterStreamWithAWS.credentials import REDDIT_CLIENT_SECRET
# from TwitterStreamWithAWS.credentials import REDDIT_PASSWORD
# from TwitterStreamWithAWS.credentials import REDDIT_USERNAME
# from TwitterSteamWithAWS.credentials import REDDIT_USER_AGENT

# from TwitterStreamWithAWS.global_params import REDDIT_DATABASE
from TwitterStreamWithAWS.global_params import (
    ALL_SUBREDDIT_REPRESETED_COUNTRY_SUBREDDIT,
    ALL_SUBREDDIT_REPRESETED_GENERAL_COVID_SUBREDDIT,
    ALL_SUBREDDIT_REPRESETED_REGION_COVID_SUBREDDIT,
    ALL_SUBREDDIT_REPRESETED_STATES_COVID_SUBREDDIT,
    STREAM_COMMENTS_DATA_KEYS,
    kinesis_reddit_stream,
    kinesis_twitter_stream,
)

# from TwitterStreamWithAWS.src.Services.RedditTwitterDataAPI.reddit_twitter_data_api_with_sqlite.update_sqlite3_database import (
#     SocialMediaDatabase,
# )
# from TwitterStreamWithAWS.src.Utilities import MyLogger

kinesis_client = boto3.client("kinesis")
REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
REDDIT_PASSWORD = os.environ.get("REDDIT_PASSWORD")
REDDIT_USERNAME = os.environ.get("REDDIT_USERNAME")
REDDIT_USER_AGENT = os.environ.get("REDDIT_USER_AGENT")

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    password=REDDIT_PASSWORD,
    user_agent=REDDIT_USER_AGENT,
    username=REDDIT_USERNAME,
)

# =====================
# == name of subreddits
# =====================
General = ALL_SUBREDDIT_REPRESETED_GENERAL_COVID_SUBREDDIT
Country = ALL_SUBREDDIT_REPRESETED_COUNTRY_SUBREDDIT
Region = ALL_SUBREDDIT_REPRESETED_REGION_COVID_SUBREDDIT
states_subreddit = ALL_SUBREDDIT_REPRESETED_STATES_COVID_SUBREDDIT

General_str = "+".join(General)
Country_str = "+".join(Country)
Region_str = "+".join(Region)
states_subreddit_str = "+".join(states_subreddit)

all_searched_subreddits = "+".join(
    [General_str, Country_str, Region_str, states_subreddit_str]
)
all_subreddit_submission_are_collected_from = {}


def get_all_class_attributes(my_class: Callable) -> List[str]:
    all_attributes = inspect.getmembers(my_class, lambda a: not (inspect.isroutine(a)))
    public_atributes = [
        a
        for a in all_attributes
        if not ((a[0].startswith("__") and a[0].endswith("__")))
    ]
    return public_atributes


# for comment in reddit.subreddit("all").stream.comments():
for comment in reddit.subreddit(all_searched_subreddits).stream.comments():

    subreddit: str = comment.subreddit

    all_comment_attributes: Dict = dict(get_all_class_attributes(comment))
    # pprint(all_comment_attributes)
    # pprint(all_comment_attributes.keys())
    # exit()

    columns_and_value_tuple_dict = all_comment_attributes

    # columns_and_value_tuple_dict: Dict[str, Any] = {
    #     i: j
    #     for i, j in all_comment_attributes.items()
    #     # if i in STREAM_COMMENTS_DATA_KEYS
    # }

    def _convert_type_to_dyamodb_type(x):
        return x

    columns_and_value_tuple_dict = _convert_type_to_dyamodb_type(
        columns_and_value_tuple_dict
    )
    # pprint(columns_and_value_tuple_dict)
    # exit()

    # timestamp_ms = str(int(columns_and_value_tuple_dict["created_utc"]))
    columns_and_value_tuple_dict['timestamp_ms']  = str(int(columns_and_value_tuple_dict["created_utc"] * 1000))
    timestamp_ms = columns_and_value_tuple_dict['timestamp_ms'] 


    def _convert_type_to_json_type(keys):

        for i in keys:
            columns_and_value_tuple_dict[i] = str(columns_and_value_tuple_dict[i])
        return columns_and_value_tuple_dict

    problem_keys = [
        "_reddit",
        "_replies",
        "all_awardings",
        "author",
        "author_flair_richtext",
        "awarders",
        "gildings",
        "mod",
        "mod_reports",
        "replies",
        "submission",
        "subreddit",
        "treatment_tags",
        "user_reports",
    ]

    # problem_keys = ["subreddit", "submission", "replies", "mod", "_reddit"]
    selected_dict = _convert_type_to_json_type(problem_keys)

    # selected_dict['lower_body'] = selected_dict['body'].lower()

    # print(selected_dict)
    # exit()

    # message = json.dumps(columns_and_value_tuple_dict)
    message = json.dumps(selected_dict)
    message = (
        message + ",\n"
    )  # NOTE: not sure what this is used for (could cause potential problem)
    print(message)

    kinesis_input_data = bytes(message, "utf-8")

    response = kinesis_client.put_record(
        StreamName=kinesis_reddit_stream,
        Data=kinesis_input_data,
        PartitionKey=timestamp_ms,
    )

    print(datetime.datetime.fromtimestamp(int(timestamp_ms) / 1000.0))
    print("--------")
