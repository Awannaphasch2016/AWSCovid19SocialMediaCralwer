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
    1. kinesis:faucovidstream_input
    2. firehose:faucovidstream_from_kinesis_to_s3
    3. s3:faucovidstream 
    4. lambda:faucovidstream 
    5. kinesis:faucovidstreamsentiment
    6. dynamoDB:faucovidstream_twitter_with_sentiment

### 

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

        

