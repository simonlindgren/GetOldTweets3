#!/usr/bin/env python3

'''
GET OLD TWEETS
Command line wrapper
Simon Lindgren 200219
'''

import got3 as got
import sqlite3
import re
import sys
import datetime

    
def main():
    print("GET OLD TWEETS")
    print("==============")
    project_setup()
    create_database()
    run_search()
    remove_duplicates()
    
    
def project_setup():
    projname = input("Project name? ")
    global dbname
    dbname = (projname + ".db")
    
    print("Searches can by done by search term(s), by username(s), or by both in combination")
    
    # QUERYSEARCH
    print("")
    print("Search terms, one or several separated by comma")
    print("Leave empty to only search by username")
    global keywords
    keywords = ""
    keywords = input('e.g. monkey,"time for bananas",#ape2020,"donkey kong": ')
    
    # USERNAMES
    print("")
    print("Usernames, one or several separated by space")
    print("Leave empty to only search by terms")
    global usernames
    usernames = ""
    usernames = input('e.g. @nintendo @jupyter (with or without the "@"): ')
    usernames = [un for un in usernames.split()]
    
    # DATES
    print("")
    print("Enter date range for search in YYYY-NN-DD format")
    global since
    since = (input("start date UTC (included in search): "))
    validate(since)
    global until
    until = (input("end date UTC (excluded from search): "))
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
    
    #MAXTWEETS
    print("")
    print("\nEnter maximum number of tweets to get per search term, or set 0 to get all possible tweets")
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
        in_reply_to TEXT,
        tweet TEXT,
        date TEXT,
        retweets INT,
        favourites INT,
        mentions TEXT,
        hashtags TEXT,
        geo TEXT)
        """)
        conn.close()
    except:
        print("A database with this name already exists")
        sys.exit()       
    
def run_search():
    
    for kw in keywords.split(","):
        
        conn = sqlite3.connect(dbname)
    
        tweetCriteria = got.manager.TweetCriteria()

        # Set the search parameters that we always set       
        tweetCriteria.setMaxTweets(maxtweets)
        tweetCriteria.setSince(since)
        tweetCriteria.setUntil(until)
        tweetCriteria.setTopTweets(toptweets)
        tweetCriteria.setEmoji("unicode")

        if len(keywords) != 0:
            tweetCriteria.setQuerySearch(kw)
        if len(usernames) != 0:
            tweetCriteria.setUsername(usernames)
        

        tweets=got.manager.TweetManager.getTweets(tweetCriteria)
        for t in tweets:
            tweet_id = t.id
            author = t.username
            in_reply_to = t.to
            tweet = t.text
            date = t.date
            retweets = t.retweets
            favourites = t.favorites
            mentions = t.mentions
            hashtags = t.hashtags
            geo = t.geo
            
            
            conn.execute('INSERT INTO tweets (tweet_id, author, in_reply_to, tweet, date, retweets, favourites, mentions, hashtags,geo) VALUES (?,?,?,?,?,?,?,?,?,?)',\
                         (tweet_id, author, in_reply_to, tweet, date, retweets, favourites, mentions, hashtags, geo))
            conn.commit()

def remove_duplicates():

    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute("CREATE TABLE temp_table as SELECT DISTINCT * FROM tweets")
    cur.execute("DELETE from tweets")
    conn.commit()

    cur.execute("INSERT INTO tweets SELECT * FROM temp_table")
    cur.execute("DELETE from temp_table")
    conn.commit()
    
    cur.execute("SELECT max(rowid) from tweets")
    n = cur.fetchone()[0]
    print("\n" + str(n) + " tweets written to database\n")
            
def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

if __name__ == '__main__':
    main()
