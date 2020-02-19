#!/usr/bin/env python3

'''
GET OLD TWEETS
Command line version
Simon Lindgren 200218
'''

import got3 as got
import sqlite3
import pandas as pd
import re
import sys
import datetime

def main():
    print("GET OLD TWEETS")
    print("==============")
    project_setup()
    create_database()
    search_compiler()
    run_search()
    end_program()
    
    
def project_setup():
    projname = input("Project name? ")
    global dbname
    dbname = (projname + ".db")
    
    print("Searches can by done by search term(s), by username(s), or by both in combination")
    
    # QUERYSEARCH
    print("")
    print("Search terms, one or several separated by space")
    print("Leave empty to only search by username")
    global keywords
    keywords = ""
    keywords = input('e.g. monkey "banana time" #ape2020 "donkey kong": ')
    
    # USERNAMES
    print("")
    print("Usernames, one or several separated by space")
    print("Leave empty to only search by terms")
    global usernames
    usernames = ""
    usernames = input('e.g. @nintendo @jupyter: ')
    
    # DATES
    print("")
    print("Enter date range for search in YYYY-NN-DD format")
    global since
    since = (input("start date: "))
    validate(since)
    global until
    until = (input("end date: "))
    validate(until)
    
    # TOPTWEETS
    print("")
    print("Do you want to get only the Top Tweets?")
    global toptweets
    top_t = input("y/n? ")
    if top_t == "y":
        toptweets = True
    else:
        toptweets = False
        
    # NEAR
    print("")
    print("Set a location to get tweets from 'near' that place, or leave blank")
    global near
    near = input("e.g. Berlin, Germany: ")
    
    # WITHIN
    print("")
    print("Set a distance radius from the 'near' location, or leave blank")
    global within
    within = input("e.g. 15km: ")
    
    #MAXTWEETS
    print("")
    print("\nEnter maximum number of tweets to get per keyword, or set 0 to get all possible tweets")
    global maxtweets
    maxtweets = (input("max tweets "))
    if maxtweets.isnumeric():
        maxtweets = int(maxtweets)
        pass
    else:
        print("You did not enter a numeric value")
        sys.exit()
        
def create_database():
    try:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        c.execute("""CREATE TABLE tweets (
        tweet_id TEXT,
        author TEXT,
        tweet TEXT,
        date TEXT,
        retweets INT,
        favourites INT,
        mentions TEXT,
        hashtags TEXT)
        """)
        conn.close()
    except:
        print("A database with this name already exists")
        sys.exit()
    
    
def search_compiler():
    global searchstring
    
    searchstring = "got.manager.TweetCriteria()"
    
    if len(keywords) > 1:
        searchstring += ".setQuerySearch(query)"
    else: pass
    if len(usernames) >1:
        searchstring += ".setUsername(usernames)"
    else: pass
    if len(near) >1:
        searchstring += ".setNear(near)"
    else: pass
    if len(within) >1:
        searchstring += ".setWithin(within)"
    else: pass
    
    searchstring += ".setSince(since).setUntil(until).setTopTweets(toptweets).setMaxTweets(maxtweets)"
    
    
def run_search():
    for kw in keywords.split():
        conn = sqlite3.connect(dbname)
        query = kw
        print("\nRunning search for " + query)
        
       

        
        #tweetCriteria = got.manager.TweetCriteria()\
        #.setQuerySearch(query)\
        #.setUsername(usernames)\
        #.setTopTweets(toptweets)\
        #.setSince(since)\
        #.setUntil(until)\
        #.setNear(near)\
        #.setWithin(within)\
        #.setMaxTweets(maxtweets)
        
        tweetCriteria = searchstring
        
        tweets = got.manager.TweetManager.getTweets(tweetCriteria)
        for t in tweets:
            tweet_id = t.id
            author = t.permalink.split("/")[3]
            tweet = re.sub("# ", "#", t.text.lower()) 
            tweet = re.sub("@ ", "@", tweet) 
            tweet = re.sub("\!|\,|\.|\?", "", tweet)
            date = str(t.date)
            retweets = t.retweets
            favourites = t.favorites
            tokens = [t for t in tweet.split() if not "/" in t]
            hashtags = " ".join([t for t in tokens if t.startswith("#")])
            mentions = " ".join([t for t in tokens if t.startswith("@")])
            conn.execute('INSERT INTO tweets (tweet_id, author, tweet, date, retweets, favourites, mentions, hashtags) VALUES (?,?,?,?,?,?,?,?)',\
                         (tweet_id, author, tweet, date, retweets, favourites, mentions,hashtags))
            conn.commit()

def end_program():
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute("SELECT max(rowid) from tweets")
    n = cur.fetchone()[0]
    print("\n" + str(n) + " tweets written to database")
    
    conn = sqlite3.connect("oldtweets.db")
    cur.execute("CREATE TABLE temp_table as SELECT DISTINCT * FROM tweets")
    cur.execute("DELETE from tweets")
    conn.commit()
    
    cur.execute("INSERT INTO tweets SELECT * FROM temp_table")
    cur.execute("DELETE from temp_table")
    conn.commit()
    
    cur.execute("SELECT max(rowid) from tweets")
    n = cur.fetchone()[0]
    print("\n" + str(n) + " tweets after duplicates removal\n")
    
    
def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

if __name__ == '__main__':
    main()
