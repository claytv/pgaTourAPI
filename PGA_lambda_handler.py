import pandas as pd
import boto3
from credentials import AWS_SECRET, AWS_ACCESS_KEY


def lambda_handler(event, context):

    bucket = 'claytvh-personal-github'

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET,
    )

    city = event['queryStringParameters']['City']
    state = event['queryStringParameters']['State']

    players_response = s3_client.get_object(Bucket=bucket, Key="players.csv")
    players_df = pd.read_csv(players_response.get("Body"))

    tournaments_response = s3_client.get_object(Bucket=bucket, Key="tournaments.csv")
    tournaments_df = pd.read_csv(tournaments_response.get("Body"))

    num_players = players_df[(players_df['City'] == city) & (players_df['State'] == state)]
    num_tournaments = tournaments_df[(tournaments_df['City'] == city) & (tournaments_df['State'] == state)]

    response = {
        'city': city,
        'state': state,
        '# Golfers': num_players,
        '# Tournaments': num_tournaments,
    }


#    city = event['queryStringParameters']['City']
 #   state = event['queryStringParameters']['State']

lambda_handler(None,None)