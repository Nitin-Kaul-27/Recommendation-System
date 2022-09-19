
"""
Code Title: Top 50 movies Extraction for Recommendation System
Created by: Nitin Kaul 

"""
import pandas as pd
import numpy as np
df = pd.read_csv("movies.csv")                                     # give the path as per your directory to read the file
print(df)
data_required = df.filter(['title','vote_count','vote_average'])
print(data_required)
m = 400
R = df['vote_average']
v = df['vote_count']
C = np.mean(df['vote_average'])
X = (v/(v+m))*R
Y = (m/(v+m))*C
data_required['weighted_score'] = X+Y
print(data_required)
data_required = data_required.sort_values(by="weighted_score",ascending=False)
popular_data = data_required.head(50)
print(popular_data)