from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np

popular_df = pickle.load(open('Top_books.pkl','rb'))
popular_movies = pickle.load(open('Top_movies.pkl','rb'))

# collab data base movie
movie_data_set = pickle.load(open('Movie_data_set.pkl','rb'))
Collab_movies_pt = pickle.load(open('Collab_movie_pt.pkl','rb'))
Collab_similarity_score_movie = pickle.load(open('Collab_similarity_scores_movies.pkl','rb'))
Collab_movie_data = pickle.load(open('Collab_Movies.pkl','rb'))

# collab data base book
Collab_books_pt = pickle.load(open('Collab_book_pt.pkl','rb'))
Collab_similarity_score_book =  pickle.load(open('similarity_scores_books.pkl','rb'))
Book_data =  pickle.load(open('Books.pkl','rb'))


# content data base movie
content_movie_data = pickle.load(open('Content_movies_data.pkl','rb'))
content_similarity_Score_movie = pickle.load(open('Content_similarity_score_movies.pkl','rb'))
content_movie_pt = pickle.load(open('Content_movies_pt.pkl','rb'))

# content data base books
content_book_data = pickle.load(open('Content_book_data.pkl','rb'))
content_similarity_Score_book = pickle.load(open('Content_similarity_score_book.pkl','rb'))
content_book_pt = pickle.load(open('Content_book_pt.pkl','rb'))

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')

@app.route('/Book')
def Book_ui():
    return render_template('Book.html',
                           book_name = list(popular_df['title'].values),
                           author=list(popular_df['author'].values),
                           image=list(popular_df['coverImg'].values),
                           rating=list(popular_df['weighted_score'].values),
                           votes=list(popular_df['numRatings'].values)
                           )

@app.route('/Movie')
def Movie_ui():  
    return render_template('Movie.html',
                           movie_name = list(popular_movies['title'].values),
                           image=list(popular_movies['Poster'].values),
                           rating=list(popular_movies['weighted_score'].values),
                           votes=list(popular_movies['vote_count'].values)
                           )

@app.route('/HOME')
def Home_ui():
    return render_template('HOME.html')

@app.route('/Book_recommend')
def Book_recommend_ui():
    return render_template('Book_recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    for i in range(1, 6):
        index3 = np.where(Collab_books_pt.index == user_input)[0][0]
        index4 = content_book_pt[content_book_pt['title'] == user_input].index[0]
        distance3 = sorted(list(enumerate(Collab_similarity_score_book[index3])), reverse=True, key=lambda x: x[1])
        distance4 = sorted(list(enumerate(content_similarity_Score_book[index4])), reverse=True, key=lambda x: x[1])
        data2 = []
        for i in range(1, 6):
            item2 = []
            j = distance3[i]
            k = distance4[i]
            temp_df1 = content_book_data[content_book_data['title'] == Collab_books_pt.index[j[0]]]
            Z1 = content_book_pt.iloc[k[0]].bookId
            Y1 = content_book_data[content_book_data['bookId'] == Z1].index[0]
            X1 = content_book_data.iloc[Y1].coverImg
            W1 = content_book_pt.iloc[k[0]].title
            U1 = [W1, X1]
            G1 = pd.DataFrame(U1)
            G1 = G1.T
            G1.columns = ['title', 'coverImg']
            item2.extend(list(temp_df1.drop_duplicates('title')['title'].values))
            item2.extend(list(temp_df1.drop_duplicates('title')['coverImg'].values))
            item2.extend(list(G1['title'].values))
            item2.extend(list(G1['coverImg'].values))

            data2.append(item2)

        print(data2)

    return render_template('Book_recommend.html', data=data2)

@app.route('/Movie_recommend')
def Movie_recommend_ui():
    return render_template('Movie_recommend.html')

@app.route('/recommend_movie', methods=['POST'])
def recommend_m():
    movie_input = request.form.get('movie_input')
    for i in range(1, 6):
        index1 = np.where(Collab_movies_pt.index == movie_input)[0][0]
        index2 = content_movie_pt[content_movie_pt['title'] == movie_input].index[0]
        distance1 = sorted(list(enumerate(Collab_similarity_score_movie[index1])), reverse=True, key=lambda x: x[1])
        distance2 = sorted(list(enumerate(content_similarity_Score_movie[index2])), reverse=True, key=lambda x: x[1])
        data1 = []
        for i in range(1, 6):
            item1 = []
            j = distance1[i]
            k = distance2[i]
            temp_df1 = content_movie_data[content_movie_data['title'] == Collab_movies_pt.index[j[0]]]
            Z = content_movie_pt.iloc[k[0]].movie_id
            Y = content_movie_data[content_movie_data['ID'] == Z].index[0]
            X = content_movie_data.iloc[Y].coverImg
            W = content_movie_pt.iloc[k[0]].title
            U = [W, X]
            G = pd.DataFrame(U)
            G = G.T
            G.columns = ['title', 'coverImg']
            item1.extend(list(temp_df1.drop_duplicates('title')['title'].values))
            item1.extend(list(temp_df1.drop_duplicates('title')['coverImg'].values))
            item1.extend(list(G['title'].values))
            item1.extend(list(G['coverImg'].values))

            data1.append(item1)

        print(data1)

    return render_template('Movie_recommend.html', data=data1)


if __name__ == '__main__':
    app.run()
