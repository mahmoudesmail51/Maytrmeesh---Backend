#import libraries
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import sqlite3

from core.models import *
from django_pandas.io import read_frame

class Recommendation():

    def recommended(item_name):

        
        # Read sqlite query results into a pandas DataFrame


        data = Item.objects.all()

        df = read_frame(data)
    
        
        #create a function to combine the values of important columns in a single string
        def get_important_features(data):
            important_features = []
            for i in range(0 , data.shape[0]):
                important_features.append(data['name'][i]+' '+ data['category'][i] + ' '+ data['description'][i])
            
            return important_features

        #add important features to dataframe
        df['important_features'] = get_important_features(df)

        #create a function that adds a column with values starting from 0 till the end
        def count(data):
            values = []
            for i in range(0,data.shape[0]):
                values.append(i)
            return values
        
        df['identifier'] = count(df)

        cm = CountVectorizer().fit_transform(df['important_features'])

        cs = cosine_similarity(cm)

        item = item_name

        item_id = df[df.name == item]['identifier'].values[0]

        scores = list(enumerate(cs[item_id]))

        sorted_scores = sorted(scores, key = lambda x:x[1], reverse= True)

        sorted_scores = sorted_scores[1:]

        #return id of the highest score
        highest_item_id = df[df.identifier == sorted_scores[0][0]]['id'].values[0]

        return(highest_item_id)