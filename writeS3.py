import pandas as pd
import io
from SportsDataPGA import SportsDataPGA
import boto3
from credentials import AWS_SECRET, AWS_ACCESS_KEY


def writeS3(df, filename, s3_client, bucket):
    '''Writes a pandas dataframe to a given s3 bucket
        :Input
            - df (DataFrame) object to write to s3
            - filename (string) name of file to be written to S3
            - s3_client (boto3.client) S3 client object with credentials
            - bucket (string) name of S3 bucket to write into

        :Returns - None
    '''

    buffer = io.StringIO()
    df.to_csv(buffer, index=False)

    response = s3_client.put_object(
        Bucket=bucket, Key=filename, Body=buffer.getvalue()
    )

    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        print(f"Successfully uploaded {filename} to S3")
    else:
        print(f"Unsuccessfully uploaded {filename} data to S3")



PGA = SportsDataPGA()

players_df = PGA.getPlayers()
tournaments_df = PGA.getTournaments()

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET
)

bucket = 'claytvh-personal-github'

writeS3(players_df, 'players.csv', s3_client, bucket)
writeS3(tournaments_df, 'tournaments.csv', s3_client, bucket)
