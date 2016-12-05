## Summarize and refine EDA:

The new features continue to correlate poorly with show cancellation.
Show runtime is a notable messy variable. A large number of shows have their runtime given in actual minutes of playtime, vs the length of the timeslot (e.g. 22 minutes vs 30 minutes). Other shows appear to have listed the sum length of the episodes, rather than the length of each episode—several have listed runtimes of hundreds of minutes. To fix this, I created a new feature for each of the main show lengths (30 and 60 minutes airtime), which include a range of times: 20-30 minutes are grouped into one variable, and 40-60 minutes are grouped into the other.


## Summarize initial results and describe how you intend to evaluate and tune:

A random forest model was used as a first benchmark for the modeling process. The training set had 1463 rows, and the test set had 488 rows.
The training set had a model score of 0.98. This is unsurprising, given that there were no parameters used to prevent over-fitting, aside from the bagging that is built into the random forest. The test set had a model score of 0.689, which is almost double the base probability of 0.35.
The confusion matrix and classification report indicate that this model is much better at predicting whether a show will be cancelled than it is at predicting whether a show will be renewed. For example, average precision is 0.67, but precision is 0.76 for renewed shows, and 0.44 for cancelled shows.
I will continue to try new models to predict show cancellation. In addition to refining the random forest using grid search, I plan to try using boosting to improve the accuracy on the cancelled shows. As previously discussed, I will also be using logistic regression, and will attempt to make a single decision tree that will be more interpretable than the bagged and boosted models.


## Describe successes, setbacks, and lessons learned along the way:

Predicting show cancellation is a difficult problem—I consider it a success that my model has any predictive power above the baseline probability.
Data quality has been a problem throughout this process. I started with almost 3000 shows, but my final dataset had just under 2000.
The analyses of plot summaries have not yet been fruitful. Both TFIDF and count vectorizer have failed to produce any helpful data.
