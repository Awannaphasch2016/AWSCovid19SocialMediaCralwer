import json
import os
import sys
import time
from datetime import datetime
from http.client import IncompleteRead  # Python 3

import boto3
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
from TwitterStreamWithAWS.global_params import kinesis_reddit_stream, kinesis_twitter_stream

# Variables that contains the user credentials to access Twitter API
consumer_key = os.environ.get("TWITTER_API_CONSUMER_KEY")
consumer_secret = os.environ.get("TWITTER_API_CONSUMER_SECRET")
access_token = os.environ.get("TWITTER_API_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_API_ACCESS_TOKEN_SECRET")


class TweetStreamListener(StreamListener):
    print("runing..................")

    # on success
    def on_data(self, data):
        print("streaming...")
        tweet = json.loads(data)
        try:
            if "text" in tweet.keys():
                message = json.dumps(tweet)
                message = (
                    message + ",\n"
                )  # NOTE: not sure what this is used for (could cause potential problem)
                print(message)

                timestamp_ms = tweet["timestamp_ms"]

                kinesis_input_data = bytes(message, "utf-8")

                response = kinesis_client.put_record(
                    # StreamName=stream_name,
                    # StreamName=kinesis_reddit_stream,
                    StreamName=kinesis_twitter_stream,
                    Data=kinesis_input_data,
                    PartitionKey=timestamp_ms,
                )

                # print(response)
                print(datetime.fromtimestamp(int(timestamp_ms) / 1000.0))
                print("--------")

        except AttributeError as ae:
            print(ae)
        except Exception as ex:
            print(ex)

        print("work fine")
        return True

    # on failure
    def on_error(self, status):
        print(status)
        return True  # always runs and do not stop at any error

    def on_exception(self, exception):
        """
           I am not sure how this is differnet from on_error.
        I also can't find info from Documentaion
        """
        print(exception)
        return


# fill the name of Kinesis data stream you created
# stream_name = "faucovidstream_input"
# stream_name = "faucovidstreamsentiment"


if __name__ == "__main__":

    # create kinesis client connection
    kinesis_client = boto3.client(
        "kinesis",
        region_name="us-east-2",  # enter the region
    )  # fill you aws secret access key

    # create instance of the tweepy tweet stream listener
    listener = TweetStreamListener()
    # set twitter keys/tokens
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # create instance of the tweepy stream
    stream = Stream(auth, listener)
    # search twitter for tags or keywords from cli parameters
    query = sys.argv[1:]  # list of CLI arguments
    query_fname = " ".join(query)  # string

    while True:

        try:
            stream.filter(track=query, stall_warnings=True)

        except IncompleteRead as ir:
            # reconnect and keep trucking
            print("the following error is caught..")
            print(ir)

            print("reconnect the network..")
            listener = TweetStreamListener()
            # set twitter keys/tokens
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            # create instance of the tweepy stream
            stream = Stream(auth, listener)
            # search twitter for tags or keywords from cli parameters
            query = sys.argv[1:]  # list of CLI arguments
            query_fname = " ".join(query)  # string
            stream.filter(track=query, stall_warnings=True)

        except Exception as ex:
            print("the following error is caught..")
            print(ex)

            print("reconnect the network..")

            listener = TweetStreamListener()
            # set twitter keys/tokens
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            # create instance of the tweepy stream
            stream = Stream(auth, listener)
            # search twitter for tags or keywords from cli parameters
            query = sys.argv[1:]  # list of CLI arguments
            query_fname = " ".join(query)  # string
            stream.filter(track=query, stall_warnings=True)
