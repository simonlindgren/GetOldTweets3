#!/usr/bin/env python3

'''
READ SQLITE3 DB INTO CSV
Simon Lindgren
200220
'''

import sqlite3
import pandas as pd
import glob

def main():
    print("\nEnter the name of a database file, located in this directory.")
    dbs = glob.glob("*.db")
    print("You have these to choose from:")
    print([i for i in dbs])
    print("\n")
    dbname = input(": ")
    print("This script assumes that there is a table named 'tweets' inside your database.")
    sql2csv(dbname)
    print("Successfully written csv!")
    
def sql2csv(dbname):
    with sqlite3.connect(dbname) as conn:
        tweets_df = pd.read_sql_query("SELECT * from tweets", conn)
        tweets_df = tweets_df.replace({'\n': ' '}, regex=True) # remove linebreaks in the dataframe
        tweets_df = tweets_df.replace({'\t': ' '}, regex=True) # remove tabs in the dataframe
        tweets_df = tweets_df.replace({'\r': ' '}, regex=True) # remove carriage return in the dataframe
        tweets_df.to_csv(dbname.split(".")[0] + ".csv", index = False)
        
if __name__ == '__main__':
    main()
