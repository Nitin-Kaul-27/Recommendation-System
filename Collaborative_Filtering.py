"""
Code Title: Collaborative filtering Algorithm for Movie Recommendation System
Created by: Nitin Kaul 

"""

import pandas as pd
import numpy as np
import ast

### ................READING DATA..........................###
movies = pd.read_csv("/movies.csv",encoding='ANSI')
credit = pd.read_csv("/credits.csv", encoding = 'ANSI')
ratings = pd.read_csv("/Ratings.csv", encoding = 'ANSI')

# Data Cleaning, checking for null values and duplicated values in the dataset, if found drop it
movies.isnull().sum()
ratings.isnull().sum()
movies.duplicated().sum()
movies.drop_duplicates(inplace=True)

# Setting the threshold to create the quality set
# Consider only those users who have rated more than 20 books
# Consider only those books which have been rated more than 20 ratings
# Play with the number to find the best value

ratings_with_movies = ratings.merge(movies,on='ID')
ratings_with_movies.groupby('user').count()['rating']
X = ratings_with_movies.groupby('user').count()['rating']> 20
users_who_gave_Rating = X[X].index
filtered_rating = ratings_with_movies[ratings_with_movies['user'].isin(users_who_gave_Rating)]
y = filtered_rating.groupby('title').count()['rating']>=20
famous_movies = y[y].index
final_ratings = filtered_rating[filtered_rating['title'].isin(famous_movies)]

# After setting the threshold, create a matrix with books in rows and users in columns
# and ratings inside the table. Every row represents the ratings given by different users to movies
# Every column represents the ratings given by one user to all the movies
pt = final_ratings.pivot_table(index = 'title', columns = 'user', values = 'rating')
pt.fillna(0, inplace=True)
pt

from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(pt)

def recommend(movie):
    index = np.where(pt.index==movie)[0][0]
    distance = sorted(list(enumerate(similarity[index])),reverse=True, key = lambda x:x[1])    # list(enumerate(similarity[index])) function wil create an index for every entry and wil help in the sorting
    for i in distance[1:6]:
        print(pt.index[i[0]])

recommend('300')
recommend('50 First Dates')
recommend('Batman Begins')
recommend('Forrest Gump')

# Note: Output may differ from the genre of input movie because in collaborative filtering, the output depends on
# similarity w.r.t other users. So the system shows you what other users are watching who are similar to you.