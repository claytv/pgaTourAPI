import pandas as pd
import io
from SportsDataPGA import SportsDataPGA
import boto3
from credentials import AWS_SECRET, AWS_ACCESS_KEY

PGA = SportsDataPGA()

players_df = PGA.getPlayers()
tournaments_df = PGA.getTournaments()

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET
)

bucket = 'claytvh-personal-github'

with io.StringIO() as csv_buffer:
    players_df.to_csv(csv_buffer, index=False)

    response = s3_client.put_object(
        Bucket=bucket, Key="players.csv", Body=csv_buffer.getvalue()
    )

    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        print("Successfully uploaded Player data to S3")
    else:
        print("Unsuccessfully uploaded Player data to S3")

    # Reset StringIO object to effectively overwrite instead of appending
    csv_buffer.seek(0)

    tournaments_df.to_csv(csv_buffer, index=False)

    response = s3_client.put_object(
        Bucket=bucket, Key="tournaments.csv", Body=csv_buffer.getvalue()
    )

    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        print("Successfully uploaded Tournament data to S3")
    else:
        print("Unsuccessfully uploaded Tournament data to S3")