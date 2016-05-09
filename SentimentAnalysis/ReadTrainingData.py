import json as json
from datetime import datetime
from pymongo import MongoClient
import csv
import fileinput
import sys
from pymongo import MongoClient

def processTweets(filename,c):    

    #load the nasdaq data...
    with open("NASDAQ.txt") as f:
        reader = csv.reader(f, delimiter="\t")
        d = list(reader)    
    
    #unzip the tuple list
    list1, list2 = zip(*d)
    tmp = list(list1[1:len(list1)]) 
    string = '$'
    Indices = [string + str(x) for x in tmp]

    keys = ["time", "user", "text"]
    values = []    
    itemsProcessed = 0
    firstLine = False
    
    with open(filename + ".txt", "r") as f:
        for line in f:            
            if firstLine == False:
                firstLine = True
                continue
            if not line.isspace():
                line_split = line.split('\t')                
                values.append(str(line_split[1].rstrip('\n')))
                if line_split[0] == 'W': 
                    itemsProcessed+=1
                    if "$" not in values[2]:
                        values = []
                        continue                                             
                    if any(x in values[2] for x in Indices):
                        print values
                        print itemsProcessed
                        c.insert_one(
                            {
                                "date" : datetime.strptime(values[0], "%Y-%m-%d %H:%M:%S"),
                                "username": values[1],
                                "text": values[2]
                             }
                            )
                        sys.stdout.write('\n')                    
                    values = []         


client = MongoClient()
db = client['TrainingData']
collection = db['Oct2009']
processTweets("tweets10",collection)