# PGATourAPI
Simple wrapper for sportsdata.io PGA Tour API and hosting of a newly developed API using AWS Lambda & API Gateway

### Goal of the project
Quickly develop a simple demo that shows the flow of HTTP requests by building an API Wrapper, injesting the information provided by the API, store it and make some basic aggregations of it available via a seperate API in a different format. 

### Files 
- ```SportsDataPGA.py``` - Wrapper for sportsdata.io PGA tour API: https://sportsdata.io/developers/api-documentation/golf#
- ```writeS3.py``` - Script that utilizes wrapper and writes data to an S3 bucket
- ```PGA_lambda_handler.py``` - script used for AWS Lambda function that is called by GET request
- ```useEndpoint.py``` - simple example of using a GET request to use the deployed API

```writeS3.py``` should be executed first to actualize the data in S3. Then it is required to setup a Lambda function using ```PGA_lambda_handler.py```. Then create a REST API in API Gateway, along with corresponding resource and GET method. Lastly, assign the previously created Lambda function to the GET method. The following endpoint is now available:  

```https://fr2srhyume.execute-api.us-west-2.amazonaws.com/demo/pga-geography```

The only parameter available for this is 'state', and the response has the following JSON

```{'state': 'CA', 'num_players': 23, 'num_tournaments': 31, 'timestamp': '2021-05-03 02:33:20'}```

- ```state``` - state passed to the endpoint
- ```num_players``` - Number of golfers born in the state
- ```num_tournaments``` - Number of tournaments in the state
- ```timestamp``` - timestamp of the request

## Example Request  
https://fr2srhyume.execute-api.us-west-2.amazonaws.com/demo/pga-geography?state=CA

## PGA Tour API Wrapper
sportsdata.io offers a limited free trial for PGA tour data. The wrapper built for this project does not support passing parameters for GET requests for two reasons, trying to keep this example simple and focused on the data flow of HTTP requests. Secondly, most of the dynamic endpoints were not supported by the free trial of this API. The following methods are available with the wrapper:  

  ```getPlayers()``` - returns a pandas dataframe of basic information about each historical PGA Tour golfer  
  ```getTournaments()``` - returns a pandas dataframe of basic information about each historical PGA Tour tournament

## Write to S3
Given the quick development time neccessary for this project, S3 was an easy decision given its ease of configuration and low cost. I shortly considered using Redshift or RDS as well but decided against it as the configuration of a full database instance has potential to be more time consuming and costly. The boto3 SDK provided by Amazon makes it very easy to interact with S3 buckets. 

## Host API Using Lambda and API Gateway
Lambda + API Gateway is an easy decision for hosting an API because of how seamlessly they work with one another. There is only one GET request implemented for this API but a variety of other requests could be added as well. When the user hits the endpoint, the Lambda function is triggered. Inside the Lambda function the data previously written to S3 is read into a pandas dataframe, then filtered to the given state and the aggregations are returned in the response. 

## Issues along the way
- Newest version of pandas says it claims support for S3 directly in ```df.to_csv()``` but i had issues with this so i used boto3 directly
- Had some issues with the StringIO() object appending instead of overwriting. I ended up reinitializing for each write. 
- Biggest struggle was getting Pandas to work properly on Lambda, first tried building my own zip file and uploading it but there was some dependency issues. I then tried pulling the dependencies using docker, but this didnt work either. I think these didnt work because I am on Mac but Lambda runs on Linux. I was finally able to get it working by using Lambda Layers and the ARN code of some pre configured layers that I found on GitHub.

## Improvements
- More endpoints and dynamic endpoints available
- Store in Redshift or RDS rather than S3. The issue with S3 is that you have to load entire dataset into Lambda function which causes performance issues. Another alternative would be to partition the data in S3 by state, however, if more parameters are available in the API this becomes less effective.  
- Make more analytics available through API hosted by Lambda + API Gateway


