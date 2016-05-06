import json as json
from datetime import datetime
from pymongo import MongoClient
import csv
import fileinput
import sys
from pymongo import MongoClient

def processTweets(filename,c):
    counter = 0
    itemsProcessed = 0

    #load the nasdaq data...    
    with open("NASDAQ.txt") as f:
        reader = csv.reader(f, delimiter="\t")
        d = list(reader)    
    
    #unzip the tuple list
    list1, list2 = zip(*d)
    tmp = list(list1[1:len(list1)]) 
    string = '$'
    Indices = [string + str(x) for x in tmp]

    #keys = ["time", "user", "text"]
    values = []    
    for line in fileinput.input(filename + ".txt"):
        if fileinput.lineno() == 1:
            continue
        if not line.isspace():
            line_split = line.split('\t')
            #sys.stdout.write(line_split[1].rstrip('\n'))
            values.append(str(line_split[1].rstrip('\n')))
            if line_split[0] == 'W':
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
                itemsProcessed+=1
                values = []

def convert_datetime(string_date):
    newtime = datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S")
    return newtime
    
         
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")

client = MongoClient()
db = client['TrainingData']
collection = db['TweetsNov2009']
processTweets("tweets11",collection)