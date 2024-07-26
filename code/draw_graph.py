import pandas as pd
import matplotlib.pyplot as plt
import boto3
from io import BytesIO
from datetime import datetime

# Initialize a session using your credentials
s3 = boto3.client('s3')

# Today's date for dynamic file access and saving
today = datetime.now().strftime("%Y-%m-%d")

# Bucket and object key for reading the CSV dynamically based on today's date
bucket_name = 'yourbucket'
object_key = f'graphs/sales_daily_{today}.csv'

# Get the object from the bucket
obj = s3.get_object(Bucket=bucket_name, Key=object_key)
# Read data from the object's body directly into a DataFrame
data = pd.read_csv(BytesIO(obj['Body'].read()))

# Remove dollar signs and commas from the 'avg_income' column
data['avg_income'] = data['avg_income'].replace({'\$': '', ',': ''}, regex=True)

# Convert the 'avg_income' column to numeric, coercing any errors
data['avg_income'] = pd.to_numeric(data['avg_income'], errors='coerce')

# Drop any rows with NaN values in 'avg_income' after conversion
data = data.dropna(subset=['avg_income'])

# Plotting the bar graph
plt.figure(figsize=(10, 8))
plt.bar(data['city'], data['avg_income'], color='blue', alpha=0.7)
plt.title('Average Income by City on ' + today)
plt.xlabel('City')
plt.ylabel('Average Income')
plt.xticks(rotation=45)

# Format y-axis to display values in a readable format
plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

# Save the plot to a BytesIO object
img_data = BytesIO()
plt.savefig(img_data, format='png')
img_data.seek(0)  # Rewind the BytesIO object

# Upload the image to S3
upload_bucket = 'uploadbucket'
upload_key = f'plots/daily_graph_{today}.png'  # You can change the directory structure if needed

s3.put_object(Bucket=upload_bucket, Key=upload_key, Body=img_data, ContentType='image/png')