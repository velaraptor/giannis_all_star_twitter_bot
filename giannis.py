import twitter
import tweepy 
from tweepy import OAuthHandler
import re
import psycopg2 as pg 
import time

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def getdatabase():
	PG_CONN_STRING = "dbname='giannis' port='5432' host='host_url' user='user' password='password'"
	dbconn = pg.connect(PG_CONN_STRING)
	return dbconn

while True:
	consumer_key = 'consumer_key'
	consumer_secret = 'consumer_secret'
	access_token = 'access_token'
	access_secret = 'access_secret'


	ourapi = twitter.Api(consumer_key='consumer_key',
	                      consumer_secret='consumer_secret',
	                      access_token_key='access_token',
	                      access_token_secret='access_secret')


	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	api = tweepy.API(auth)


	##run every hour and search based on time and add to query 
	results_giannis = api.search(
	    q="%23nbavote+giannis", count = 15)

	##results_userhandle = api.search(
	##    q="%40Giannis_An34+%23nbavote", count = 15)
	##filter out words that have Giannis antetokounmpo
	##if doesnt have antetokounmpo, tell them to put this name 

	results_mispelling = api.search(
	    q="%23nbavote+antetokoumpo", count = 15)

	for tweet in results_giannis :
		screen_name = tweet.user.screen_name
		text = tweet.text
		dbconn = getdatabase()
		cursor = dbconn.cursor()
		cursor.execute("SELECT COUNT(screen_name)FROM user_names WHERE screen_name = {!r}".format(screen_name))
		screen_name_count = cursor.fetchall()
		if(screen_name_count[0][0] > 0):
			print("Already Done!")
		else:
			cursor.execute("INSERT INTO user_names(screen_name) VALUES({!r})".format(screen_name))
			dbconn.commit()
			if(findWholeWord("Antetokounmpo")(text)):
				print("Good!")
			else:
				tweet_to_send = "@"+screen_name+" Hey make sure to add Giannis' full name! It's Giannis Antetokounmpo!"
				status = ourapi.PostUpdate(tweet_to_send)
		cursor.close()
		dbconn.close()

	for tweet in results_mispelling :
		screen_name = tweet.user.screen_name
		text = tweet.text
		dbconn = getdatabase()
		cursor = dbconn.cursor()
		cursor.execute("SELECT COUNT(screen_name) FROM user_names WHERE screen_name = {!r}".format(screen_name))
		screen_name_count = cursor.fetchall()
		if(screen_name_count[0][0] > 0):
			print("Already Done!")
		else:
			cursor.execute("INSERT INTO user_names(screen_name) VALUES({!r})".format(screen_name))
			dbconn.commit()
			tweet_to_send = "@"+screen_name+" Hey make sure to spell Giannis' last name right! It's Giannis Antetokounmpo!"
			status = ourapi.PostUpdate(tweet_to_send)
		cursor.close()
		dbconn.close()
	time.sleep(900)
