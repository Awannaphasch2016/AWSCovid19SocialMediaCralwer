#! /bin/bash

rm -rf lambda_s3_to_dynamo_with_api.zip 
zip -r lambda_s3_to_dynamo_with_api.zip .
aws lambda update-function-code --function-name  faucovidstream --zip-file fileb://lambda_s3_to_dynamo_with_api.zip
