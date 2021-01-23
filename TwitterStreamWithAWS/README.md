# AWS <service:resources>

## Streams

### Kinesis -> S3 -> Lambda -> DynamoDB
* kinesis:faucovidstream_input
* s3:faucovidstream 
* lambda:faucovidstream
* dynamoDB:faucovidstream_twitter_with_sentiment
* APIGateway:KinesisProxy

# Directory 
* src/
    * description: main code that will run in production
    * Consumers/
        * description: each modules are consumer of one or more producer.  
    * LambdaAPIDynamodb/
        * description: producers that have the following workflow API -execute-> Lambda -manipulate-> DynamoDB
* Example/
    * description: example code 
    * Demo/ 
        * description: project-base example. 
    * Libraries/
        * description: example based on libraries being used

        

