
"""
Code Title: Content based Algorithm  + Collaborative Filtering Combined for Movie Recommendation System
Created by: Nitin Kaul 

"""
import pandas as pd
import numpy as np
import ast

### ................READING DATA..........................###
movies = pd.read_csv("/movies.csv",encoding='ANSI')
credit = pd.read_csv("/credits.csv", encoding = 'ANSI')
ratings = pd.read_csv("/Ratings.csv", encoding = 'ANSI')
movies_c = movies

# ................Content Filtering ...................#
movies = movies.merge(credit,on='title')
colnames = movies.keys()                                        # extracting column names to check which attribute to keep and which to remove
#print(colnames)
movies = movies.filter(['movie_id','title','genres','overview','keywords','cast','crew'])
A = movies['genres'][0]
B = movies['cast'][0]
C = movies['crew'][0]
D = movies['keywords'][0]

def extract_name(text):
    L = []
    for i in ast.literal_eval(text):            		# ast.literal_eval() converts the entire structure into lists by recognizing the pattern
        L.append(i['name'])                      		# as per the data in every list, the function searches for the name
    return L


movies.dropna(inplace=True)
movies['genres'] = movies['genres'].apply(extract_name)         # Extracts name from genres
movies['cast'] = movies['cast'].apply(extract_name)             # Extracts name from cast
movies['keywords'] = movies['keywords'].apply(extract_name)     # Extracts name from keywords


def director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L 

movies['crew'] = movies['crew'].apply(director)                 # Extracts name from job type director

A = movies['genres'][0]
B = movies['cast'][0]
C = movies['crew'][0]
D = movies['keywords'][0]

def collapse(L):
    L1 = []
    for i in L:
        L1.append(i.replace(" ",""))
    return L1

movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(collapse)
movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)
movies.dropna(inplace=True)
movies['overview'] = movies['overview'].apply(lambda x:x.split())
A = movies['genres'][0]
B = movies['cast'][0]
C = movies['crew'][0]
D = movies['keywords'][0]

movies['tags'] = movies['genres'] + movies['cast'] + movies['crew'] + movies['keywords'] + movies['overview']
movies.isnull().sum()

final_movie_data = movies.drop(columns = ['genres','cast','crew','overview','keywords'])
final_movie_data['tags'] = final_movie_data['tags'].apply(lambda x: " ".join(x))         # In this step, all the tags are joined together to create a single string
final_movie_data['tags'][0]

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')
vector = cv.fit_transform(final_movie_data['tags']).toarray()
vector.shape

from sklearn.metrics.pairwise import cosine_similarity
similarity1 = cosine_similarity(vector)

final_movie_data[final_movie_data['title'] == 'The Lego Movie'].index[0]

#%%
#.........................COLLABORATIVE.......................#

movies_c.isnull().sum()
ratings.isnull().sum()

movies_c.duplicated().sum()
movies_c.drop_duplicates(inplace=True)
ratings_with_movies = ratings.merge(movies_c,on='ID')
ratings_with_movies.groupby('user').count()['rating']

X = ratings_with_movies.groupby('user').count()['rating']> 20
users_who_gave_Rating = X[X].index
filtered_rating = ratings_with_movies[ratings_with_movies['user'].isin(users_who_gave_Rating)]

y = filtered_rating.groupby('title').count()['rating']>=20
famous_movies = y[y].index
final_ratings = filtered_rating[filtered_rating['title'].isin(famous_movies)]

pt = final_ratings.pivot_table(index = 'title', columns = 'user', values = 'rating')
pt.fillna(0, inplace=True)
pt

similarity2 = cosine_similarity(pt)

#%%

#.................. Creating Recommend function......................#
def recommend(movie):
    index1 = final_movie_data[final_movie_data['title'] == movie].index[0]
    index2 = np.where(pt.index==movie)[0][0]
    distance1 = sorted(list(enumerate(similarity1[index1])),reverse=True, key = lambda x:x[1])     # list(enumerate(similarity[index])) function wil create an index for every entry and wil help in the sorting
    distance2 = sorted(list(enumerate(similarity2[index2])),reverse=True, key = lambda x:x[1])
    print("------------------------------------------------")
    print("----You have asked for recommendation related to movie : ", movie,"----")
    print("...TOP 5 similar movies to ",movie," are...")
    for i in distance1[1:6]:
        print(final_movie_data.iloc[i[0]].title)
    print("---------------------------------------------")
    print("...Similar Users also liked these movies...")
    for i in distance2[1:6]:
        print(pt.index[i[0]])
    
    
#%%
### ................OUTPUT..........................###   
recommend('Die Hard')     
recommend('The Dark Knight')
recommend('Gandhi')
recommend('A Beautiful Mind')
recommend('A Walk to Remember')
recommend('Avatar')
recommend('Batman Begins')
recommend('Dumb and Dumber')
recommend('Pirates of the Caribbean: On Stranger Tides')
recommend('Midnight Cowboy')

