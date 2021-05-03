import pandas as pd
import json
import boto3
import datetime


def lambda_handler(event, context):

    """Lambda function associated with
        https://fr2srhyume.execute-api.us-west-2.amazonaws.com/demo/pga-geography endpoint"""

    bucket = 'claytvh-personal-github'
    # AWS_ACCESS_KEY = credentials.AWS_ACCESS_KEY
    # AWS_SECRET = credentials.AWS_SECRET

    # Hide Credentials
    AWS_ACCESS_KEY = ''
    AWS_SECRET = ''

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET,
    )

    state = event['queryStringParameters']['state']

    # Read players dataframe from S3
    players_response = s3_client.get_object(Bucket=bucket, Key="players.csv")
    players_df = pd.read_csv(players_response.get("Body"))

    # Read tournaments data from S3
    tournaments_response = s3_client.get_object(Bucket=bucket, Key="tournaments.csv")
    tournaments_df = pd.read_csv(tournaments_response.get("Body"))

    # Number of players and number of tournaments from the city and state passed as parameters
    num_players = players_df[(players_df['BirthState'] == state)].shape[0]
    num_tournaments = tournaments_df[(tournaments_df['State'] == state)].shape[0]

    # Body of the response
    responseBody = {}
    responseBody['state'] = state
    responseBody['num_players'] = num_players
    responseBody['num_tournaments'] = num_tournaments
    responseBody['timestamp'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    # Entire HTTP response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['body'] = json.dumps(responseBody)

    return responseObject


