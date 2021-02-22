# AWS <service:resources>

## Streams

### API -> DynamoDB -> Lambda 
* description: access dynamodb data via api gateway
* kinesis:faucovidstream_input
* dynamoDB:faucovidstream_twitter_with_sentiment
* APIGateway:KinesisProxy


### Kinesis -> S3 -> Lambda -> DynamoDB
* description: store original stream data in S3, and store modified data in DynamoDb
*  workflow step by step:
    1. kinesis
        * raw input stream
            * twitter -> faucovidstream_input
            * reddit -> faucovidstream_input_from_reddit
    2. firehose
        * twitter -> faucovidstream_from_kinesis_to_s3
        * reddit -> faucovidstream_from_reddit_input_kinesis_to_s3
    3. s3
        * twitter -> faucovidstream
        * reddit ->  faucovidstreamreddit
    4. lambda
        * twitter -> faucovidstream
        * reddit -> faucovidstream_reddit
    5. kinesis
        * modified input stream (with sentiment)
            * twitter -> faucovidstreamsentiment
            * reddit -> faucovidstreamsentiment_reddit
    6. dynamoDB
        * twitter -> faucovidstream_twitter_with_sentiment 
        * reddit -> faucovidstream_reddit_with_sentiment

# Directory 
* src/
    * description: main code that will run in production
    * Consumers/
        * description: each modules are consumer of one or more producer.  
    * LambdaAPIDynamodb/
        * description: producers that have the following workflow API -execute-> Lambda -manipulate-> DynamoDB
    * LambdaWithS3TriggerLinuxPy36/
        * description: 
* Example/
    * description: example code 
    * Demo/ 
        * description: project-base example. 
    * Libraries/
        * description: example based on libraries being used

        

