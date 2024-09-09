import pprint
import requests
from datetime import datetime, timedelta

import tweepy

# Twitter API credentials 
API_KEY = 'PUT_HERE_TOKEN'
API_SECRET_KEY = 'PUT_HERE_TOKEN'
ACCESS_TOKEN = 'PUT_HERE_TOKEN'
ACCESS_TOKEN_SECRET = 'PUT_HERE_TOKEN'
BEARER_TOKEN = 'PUT_HERE_TOKEN'

# Authenticate to Twitter using the v2 API
client = tweepy.Client(bearer_token=BEARER_TOKEN,
                       consumer_key=API_KEY,
                       consumer_secret=API_SECRET_KEY,
                       access_token=ACCESS_TOKEN,
                       access_token_secret=ACCESS_TOKEN_SECRET)


secret = "PUT_HERE_TOKEN"
url = 'https://newsapi.org/v2/top-headlines?'

parameters = {
	#'category': 'technology',
	#'q': 'technology', 
	'pageSize': 100, 
    #'country': 'us',
    'sources': 'bbc-news',
    #'page': '10',
	'apiKey': secret 
}

# Make the request
response = requests.get(url, params=parameters)

# Convert the response to JSON format
response_json = response.json()

# Get yesterday's date
yesterday = (datetime.utcnow() - timedelta(days=1)).date()

# Prepare output list
output_list = []

# Process articles
for article in response_json.get('articles', []):
    description = article.get('description')
    source = article.get('source', {}).get('name')
    published_at = article.get('publishedAt')

    # Check if description, source, or publishedAt is empty or "none"
    if not description or not source or not published_at:
        continue

    # Check if publishedAt is yesterday
    published_date = datetime.fromisoformat(published_at.replace('Z', '')).date()
    if published_date != yesterday:
        continue

    if len(description) > 80:
        description = description[:130]
        if '.' in description:
            description = description[:description.rfind('.') + 1]

    # Create a formatted string
    formatted_string = f"{description[:130]}"
    
    # Check the length of the output string
    if len(formatted_string) <= 260:
        output_list.append(formatted_string)

# Pretty print the output list
#pprint.pprint(output_list)
output_list2 = '\n\n'.join(sentence.strip("'") for sentence in output_list)
output = "Daily Top News\n\n" + output_list2
truncated_output = output[:280]
print(truncated_output)
print("\n")

try:
    client.create_tweet(text=truncated_output)
    print(f"Tweeted: {truncated_output}")
except Exception as e:
    print(f"Error while tweeting: {e}")


