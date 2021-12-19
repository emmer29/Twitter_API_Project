import json
import tweepy as tw
import gspread
import pandas as pd
from key_folder.keys import *
from oauth2client.service_account import ServiceAccountCredentials
import pprint

# Authenticate twitter API
auth = tw.OAuthHandler(my_api_key, my_api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Authenticate gspread for google spreadsheet
scope = [
    "https://spreadsheets.google.com/feeds",
    'https://www.googleapis.com/auth/spreadsheets',
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
cred = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
client = gspread.authorize(cred)

# Create new spreadsheet and share
# new_sheet = client.create('twitter_jobs')
sheet = client.open('twitter_jobs').sheet1
# sheet.share('api-project@my-api-project-333921.iam.gserviceaccount.com',
# perm_type='user', role='writer'
# )

# Define query parameters to fetch response from twitter API

# search_query = input("Software Developer Jobs -filter:retweets")
# time_id = input("Enter time frame: ")
search_query = "Software Developer Jobs -filter:retweets"
tweets = tw.Cursor(api.search_tweets,
                   q=search_query,
                   lang="en", since_id="2021-12-03").items(20)

# "Software Developer Jobs -filter:retweets

# Store the object response by storing in a list
tweets_copy = []

for tweet in tweets:
    tweets_copy.append(tweet)
    # pprint.pprint(list(tweets_copy))

# Looping response & storing items of interest in a flat dict
job_data = []

for x in tweets_copy:
    job_item_dict = {
        "JOB DESCRIPTION": x._json['text'],
        "JOB LINK": x.entities['urls'][0]['expanded_url'],
        "JOB SOURCE": x.source,
        "LOCATION": x._json.get('user', {}).get('location', {}),
        "LANGUAGE OF POST": x.metadata['iso_language_code']
    }

    job_data.append(job_item_dict)

# Quick format list of dictionary for easy write to spreadsheet

df = pd.DataFrame(job_data)
print(df.head())
sheet.update([df.columns.values.tolist()])  # + df.values.tolist())

# filter the goole sheets based on location or keyword

sheet = client.open('twitter_jobs').sheet1
