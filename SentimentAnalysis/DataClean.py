# import modules necessary for all the following functions
import re
import pandas as pd
from sklearn import preprocessing
import json
from RAKE import Rake
import operator
from nltk.corpus import stopwords
import string
import json as json
from datetime import datetime

def readJson(filename):
    """
    reads a json file and returns a clean pandas data frame
    """

    import pandas as pd
    df = pd.read_json(filename)  
       
    
    #allows us join all the subarrays in keywords
    def unlist(element):
        return ''.join(element)
    
    for column in df.columns:
        df[column] = df[column].apply(unlist)       
    # gets only first 10 characters of date: year/month/day
    df['date'] = df['date'].apply(lambda x: x[:10])  
    df['date'] = pd.to_datetime(df['date'])   
    
    for index, row in df.iterrows():
        if row['keywords'] == "":
            df.set_value(index,'keywords', giveKeyword(row['body']))                       

    #sort the columns by date
    df = df.sort(columns = 'date')
    df['body'] = df['body'].apply(cleanText) ##clean the data a final time
    
    # use ix to reorder
    df = df.ix[:, ['date', 'keywords', 'body']]    
    return df

def cleanText(text):
    """
    removes punctuation, stopwords and returns lowercase text in a list of single words
    """
    text = text.lower()    
    
    from bs4 import BeautifulSoup
    text = BeautifulSoup(text,"lxml").get_text()   
    
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    text = tokenizer.tokenize(text)
    #print text
   
    clean = [word for word in text if word not in stopwords.words('english')]  

    return clean

def to_json(df,filename):
    d = [ 
        dict([
            (colname, row[i]) 
            for i,colname in enumerate(df.columns)
        ])
        for row in df.values
    ]
    return json.dump(d, open(filename + '.json', 'w'),indent = 1,default=json_serial)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")

def giveKeyword(text):
    from bs4 import BeautifulSoup
    text = BeautifulSoup(text,"lxml").get_text()   
    
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    text = tokenizer.tokenize(text)
    #print text

    cleanText = "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in text]).strip()    

    rakeobj = Rake("SmartStoplist.txt")        
    keywords = rakeobj.run(cleanText)
    
    output = keywords[0][0] + "," + keywords[1][0]

    return output  #the highest ranked one...
currentDf = readJson('result.json')
to_json(currentDf, 'CleanedData')

#now we need to find a way to format and save as json or csv......
nargb = 1
