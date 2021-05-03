# pgaTourAPI
Simple wrapper for sportsdata.io pga tour API and hosting of a newly developed API using AWS Lambda & API Gateway

### Goal of the project
Quickly develop a simple demo that show the flow of HTTP requests by building an API Wrapper, injesting the information provided by the API, store it and make some basic aggregations of it available in a different format. 

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

## PGA Tour API Wrapper
sportsdata.io offers a limited free trial for PGA tour data. The wrapper built for this project does not support passing parameters for GET requests for two reasons, trying to keep this example simple and focused on the data flow of HTTP requests. Secondly, most of the dynamic endpoints were not supported by the free trial of this API. The following methods are available with the wrapper:  

  ```getPlayers()``` - returns a pandas dataframe of basic information about each historical PGA Tour golfer  
  ```getTournaments()``` - returns a pandas dataframe of basic information about each historical PGA Tour tournament

## Write to S3
Given the quick development time neccessary for this project, S3 was an easy decision given its ease of configuration and low cost. I shortly considered using Redshift as well but decided against it as the configuration of Redshift has potential to be more time consuming and costly. The boto3 SDK provided by Amazon makes it very easy to interact with S3 buckets. 

## Host API Using Lambda and API Gateway
Lambda + API Gateway is an easy decision for hosting an API because of how seamlessly they work with one another. There is only one GET request implemented for this API but a variety of other requests could be added as well. When the user hits the endpoint, the Lambda function is triggered. Inside the Lambda function the data previously written to S3 is read into a 
