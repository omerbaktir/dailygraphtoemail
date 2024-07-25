import boto3
import json
import pandas as pd
import psycopg2
from io import StringIO
from datetime import datetime
import os

def lambda_handler(event, context):
    # PostgreSQL connection parameters
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_port = os.getenv("DB_PORT", "5432")  # default PostgreSQL port

    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port
        )
        
        cursor = connection.cursor()
        
        # Execute a query
        cursor.execute("SELECT city, sum(yearlyincome) as avg_income FROM prospectivebuyer group by city order by avg_income desc limit 10;")
        
        columns = [desc[0] for desc in cursor.description]
        result = cursor.fetchall()
        
        # Convert result to a Pandas DataFrame
        df = pd.DataFrame(result, columns=columns)
        
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)

        # Create an S3 client
        s3_client = boto3.client('s3')
        today_date = datetime.now().strftime('%Y-%m-%d')

        # Upload CSV to S3
        bucket_name = 'yourbucket'
        object_name = f'files/sales_daily_{today_date}.csv'
        s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=csv_buffer.getvalue())
        
        # Close the cursor and connection
        cursor.close()
        connection.close()
        
        print(df)
        
        # Return the result as JSON
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }