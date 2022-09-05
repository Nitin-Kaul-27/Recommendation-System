
# This is a data cleaning code for the movie database.

# The given database has 2 files, movies and credit. They are merged before starting the cleaning process
# In the file, the columns Genre, Cast, Crew, Keywords has a lot of symbols, special characters, and we are required to find the specific characters in every row of these 4 columns

# All these has many values which are not required, after cleaning, only the genre, actors in the movies, crew involved in the movie, and 
# specific keywords of the given movie will stay in row, and rest of the data will be cleaned



library(stringr)
library(tidyr)
library(dplyr)
library(fedmatch)
movie <- read.csv(file.choose(),na.strings = " ")
credit <- read.csv(file.choose(), na.strings = " ")
data <- merge(movie,credit,by="title")
data <- data[,c('movie_id','title','genres','cast','keywords','crew','overview')]

# Removing of empty data, which was not shown as NULL or NA value, 
# All these rows Had TRUE condition for complete case
# Thus, calculated the word count in each row and removed if word count is just 1
# Package used here for cleaning was FEDMATCH
y <- data[,3:6]
all_indexes <- list()
for (k in 1:ncol(y)) {
  x <- y[,k]
  index <- 0
  count <- 1
  for (i in 1:length(x)) {
    w=word_frequency(x[i])        # counts the word frequency 
    if(nrow(w)==1){
      index[count] <- i
      count <- count+1
    }
  }
  all_indexes[k] <- list(index)
}
index <- unlist(all_indexes)
data <- data[-index,]

# Cleaning the Content
# In this part, curly braces were removed, data was splitted and specific characters were extracted
# In all the columns, function is searching for the keyword "name" and returning the corresponding value
# package used for cleaning here was STRINGR
y <- data[,3:6]
count <- 3
for(k in 1:4){
  x <- y[,k]
  x <- as.data.frame(x)
  for (i in 1:nrow(x)) {
    c <- 0
    a <- str_extract_all(x[i,1],"(?<=\\{).+?(?=\\})")[[1]]    # extracting data between the curly brackets
    for (j in 1:length(a)) {
      l=gsub('"','',a[j])
      m=strsplit(l,split=",")                                 # strsplit function is used to split the string and gives list as an output, "," is used as a separator here
      m=as.data.frame(m)
      o=grepl("name",m[,1])                                   # grepl function is used to find a specific word in the column
      m=m[which(o[]==TRUE),]
      m=as.data.frame(strsplit(m,split=": "))                 # spliting again being done by ": " as a separator
      m=m[2,]
      c[j] = m
      c[j] = gsub(" ","",c[j])                                # gsub function removes the unwanted pattern from the string
    }
    c = paste(c, collapse = ', ')                             # paste function here is used to remove the spacing between the required name
    x[i,1] = c 
  }
  data[,count] <- x
  count <- count+1
}


