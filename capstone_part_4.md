## 1) What is your question?
The dependent variable is whether or not a show got cancelled in its first season. Shows were considered to have been cancelled in the first season if the number of seasons listed on IMDB was 1.

Independent variables fall into three categories: (1) descriptive features of the show, including keywords, genre, and runtime, (2) the timing of the show, such as the year, month and day it was released, and (3) a text analysis of the plot descriptions from IMDB.

## 2) What is your data?
A list of titles of American TV shows since 1980 was taken from Wikipedia. From these titles, data was taken from OMDbAPI, IMDB’s API. All data was taken from this api, except for distribution network, which was scraped from IMDB directly.
Most variables required transformation to be useable. Dummy variables were created for month and day of the week. Year and day of the month were separated, but kept as integers. Each genre listed by IMDB, as well as the most common keywords were turned into dummy variables. Dummy variables were also created for 1/2 hour and full hour shows.

For the plot summaries, a TFIDF was used  in an attempt to find words that are more common in cancelled or renewed shows. This yielded approximately 10000 columns of unique words, which needed to be reduced to a manageable size. Principal component analysis was used to accomplish this. In the first attempt, 750 components were extracted from the original 10000.

## 3) Potential models?
This project is a classification problem, so a classifier model must be used. Three models will eventually be created: a logistic regression, a single decision tree, and an ensemble model. A logistic regression will be used because it is the most interpretable of the applicable models. People will be interested in knowing what features of a new show will make it more or less likely to be cancelled, and a logistic regression will provide that, even though it will not yield the best predictive power. A single decision tree will be the next-best option for people who are interested in using individual features of a new show to predict its future. A decision tree, although difficult to implement well, will offer an easy-to-follow guide for people interested in a new show. An ensemble model, such as a random forest, is likely to offer the best predictive power of any model, although it is not possible for humans to interpret it on the fine scale.

## 4) Results
The only models that have currently been built so far are random forests. These have yielded a maximum model score of 0.70 on previously-unseen data.
The analysis of the plot summaries has not yet been fruitful.

## 5) Answer your original question!
This project demonstrates that TV cancellation is a predictable phenomenon. In this first iteration, the text analysis may not be fruitful. With more work, this may add predictive power to the model.

Some important variables were not available for this analysis--notably timeslot. This data may be available in the future, and may improve the model. 
