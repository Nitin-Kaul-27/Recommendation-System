
"""
Code Title: Content based Algorithm for Recommendation System
Created by: Nitin Kaul 

"""
import pandas as pd
import numpy as np
import ast

### ................READING DATA..........................###
movies = pd.read_csv("movies.csv")                                                        # give the path as per your directory to read the file 
credit = pd.read_csv("credits.csv")

# MERGING 2 FILES, EXTRACTING REQUIRED COLUMNS
# DATA 1 has all the movie details, their ID, Title, keywords, overview, budget, average ratings
# DATA 2 has mainly the details of cast and creq which is associated with the movie
movies = movies.merge(credit,on='title')
colnames = movies.keys()                                                                   # extracting column names to check which attribute to keep and which to remove
print(colnames)
movies = movies.filter(['movie_id','title','genres','overview','keywords','cast','crew'])

### ................DATA CLEANING..........................###

# After merging the data and keeping the required columns, data was cleaned to extract all the necessary information
# Required information: 
# Exact names of Genres, Exact keywords, Names of cast, director, and storyline
A = movies['genres'][0]
B = movies['cast'][0]
C = movies['crew'][0]
D = movies['keywords'][0]
print(A)
print(B)
print(C)
print(D)

# To extract the exact required information a function is created to look into the structure and extract only the name in it
# For this ast (Abstract Syntax Tree) library is used
# This library helps to read the grammer in the structure
def extract_name(text):
    L = []
    for i in ast.literal_eval(text):             # ast.literal_eval() converts the entire structure into lists by recognizing the pattern
        L.append(i['name'])                      # as per the data in every list, the function searches for the name
    return L
movies.dropna(inplace=True)
movies['genres'] = movies['genres'].apply(extract_name)         # Extracts name from genres
movies['cast'] = movies['cast'].apply(extract_name)             # Extracts name from cast
movies['keywords'] = movies['keywords'].apply(extract_name)     # Extracts name from keywords


# In the crew data, there was a change as the name was under the cateogry of job
# So before finding the name it was important to find the job type and then the name
def director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L 

movies['crew'] = movies['crew'].apply(director)                  # Extracts name from job type director

A = movies['genres'][0]
B = movies['cast'][0]
C = movies['crew'][0]
D = movies['keywords'][0]
print(A)
print(B)
print(C)
print(D)

# Once all the names were extracted, all the sapces were removed between the characters
# This was done to ignore any issues while searching
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
print(A)
print(B)
print(C)
print(D)

movies['tags'] = movies['genres'] + movies['cast'] + movies['crew'] + movies['keywords'] + movies['overview']
movies.isnull().sum()

final_movie_data = movies.drop(columns = ['genres','cast','crew','overview','keywords'])
final_movie_data['tags'] = final_movie_data['tags'].apply(lambda x: " ".join(x))         # In this step, all the tags are joined together to create a single string
final_movie_data['tags'][0]

### ................DATA PROCESSING..........................###

# Step 1 in data processing is to do the Vectorization
# Vectorization was done using the concept of Bag of words by converting words into numbers
# A matrix is created which gives the count of every common tag in its bucket of tags
# All the tags of entire data were collected together nd 5000 most common words were extracted
# Then every tag was counted in the individual movie Tag for its frequency.
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')
vector = cv.fit_transform(final_movie_data['tags']).toarray()
#vector.shape

# Step 2 after creating the tag vector was to find the similarity between the movies
# Similarity is calcuated using cosine similarity due to the size of data
# output is a nxn size array which gives similarity of every individual movie with another movie.
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vector)

final_movie_data[final_movie_data['title'] == 'The Lego Movie'].index[0]

# Step 3 is to create a function which can return the recommended movie list
# Till this point we have an array which has the similarity score of every movie based on their tags
# This function takes a movie name, finds its index and sorts the similarity column in descending order
# Finally returns 5 top movies
def recommend(movie):
    index = final_movie_data[final_movie_data['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])),reverse=True, key = lambda x:x[1])     # list(enumerate(similarity[index])) function wil create an index for every entry and wil help in the sorting
    for i in distance[1:6]:
        print(final_movie_data.iloc[i[0]].title)

### ................OUTPUT..........................###        
recommend('The Dark Knight')
recommend('Gandhi')
recommend('A Beautiful Mind')
recommend('A Walk to Remember')
recommend('Avatar')
recommend('Batman Begins')
recommend('Dumb and Dumber')
recommend('Pirates of the Caribbean: On Stranger Tides')
