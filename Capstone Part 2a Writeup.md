## Articulate specific aim:

The goal of this is to predict whether a tv show will be cancelled in its first season.


## Outline proposed methods and models:

Shows that began prior to 2016 and lasted for only one season are considered to have been cancelled. The independent variables will be features that describe the details of the shows. These will include runtime, genre, keywords, timeslot, as well as text analysis of the plot description and title.
The most predictive model for this type of analysis will be a decision tree-type model, because there will likely be non-linear relationships among the variables. However, people will be very interested in knowing what features predict cancellation, and in what ways. For this reason, three types of models will be created:
1) Logistic regression: a logistic regression will be attempted because it is the easiest to interpret.
2) Single decision tree: a single decision tree will be attempted because it will be possible to show the steps that the model takes to make predictions.
3) Ensemble decision tree: using boosting or bagging, an ensemble model will be used to make as predictive a model as possible.

## Define risks and assumptions:

#### Risks:
1) This project is fundamentally risky. This question is important to a very large industry, and I doubt I am the first to attempt it. The question I am asking may be beyond the scope of this project.
2) Data is limited. The kind effect I am looking for may not be detectable with this sample size.
Data is limited, what I have may not be good enough to do what I want to do.

I may not have access to all of the data I want or need

#### Assumptions:
1) This analysis treats shows with only one season as having been cancelled rather than being miniseries that were only intended to have one season.
2) This dataset is as large as I could make it, but it still may not be complete. This analysis assumes that the data included are representative of all of American TV shows.
3) Of my initial data, about 300 rows have had to be removed due to missing data. This analysis assumes that the absence of these shows will not be fundamentally different than their presence.


## Revise initial goals and success criteria as needed:

n/a

## Create local database/dataset:

Initially, a list of American TV shows from 1990 forward was scraped from http://www.crazyabouttv.com/. This yielded fewer titles than hoped, so it was abandoned.
A wikipedia page was found that contains a long list of American TV shows (https://en.wikipedia.org/wiki/List_of_American_television_programs_by_date). Scraping was attempted on this page, but the shows were listed in an inconsistent format, making scraping difficult. In the end, the titles were copied by hand, pasted into an excel spreadsheet, and converted to .csv format.
Using IMDB’s API, basic information about each show was downloaded in json format. The items in the json were then parsed into their own columns.
Keywords were not accessible from the api, so they were scraped directly from IMDB.

## Describe data cleaning/munging techniques:

Most of the data in this dataset required cleaning. The titles copied from Wikipedia had data fragments attached—these were separated and cleaned using the split function. The strip function was then used to remove lingering spaces. All of the data taken from the api were in str format. Missing data was noted as ’n/a’, which had to be changed before a column containing numeric data could be converted into int or float format.
Some shows could not be found by entering the title into the api (the search function on IMDB is fairly poor at recognizing titles that are entered slightly differently). These rows were removed.
Runtime was given in “XX min” format—the ‘min’ was removed using the split function, and the numbers were converted to int format. For some shows, runtime appears to be given as the cumulative number of minutes the series ran for, rather than the length of each episode. These will need to be parsed somehow or removed.



## Create data dictionary:

‘json’: the initial json retrieved through imdbpie. This did not contain as much information as was hoped for.
‘title_rough’: the show title with data fragment taken from Wikipedia
‘check’: a column used to find missing data
‘title’: the cleaned version of the show titles
‘imdb_id’: the ID used by IMDB to identify unique shows
‘big_json’: the json retrieved through OMDB api, when imdbpie failed to return sufficient information.
‘seasons’: the number of seasons that a show ran for
‘cancelled’: 1 if seasons==1, 0 if seasons > 1.
‘runtime’: str version of runtime
‘genres’: all of the genre tags associated with a show
‘parental_rating’: the parental advisory rating for the show
‘imdb_rating’: the average user review for the show (1-10)
‘release_date’: the day, month and year that the show first aired on.
‘plot’: the long-form plot summary of the show
‘year’: the year in which the show was released, in str format. Sometimes includes end year.
‘type’: the category into which IMDB places an entry (e.g. tv series, movie)
‘votes’: the number of IMDB users who rated the show
‘metascore’: aggregation of critical review scores
‘keywords’: keywords associated with the show
‘first_year’: the year in which the show was released, cleaned and in int format.
‘is_new’: 1 if the show was released in 2015 or 2016, 0 if released in 2014 or earlier.
‘fixed_runtime’: the show runtime in int format.


## Perform and summarize EDA:

Out of 2590 shows, 901 of them appear to have been cancelled in the first season, for a base probability of 0.35.
Mode IMDB rating is 7.
Median ‘first_year’ is 2005. This is also approximately the mode.
Excluding shows with a reported runtime of over 100 minutes, most shows have a runtime of approximately 30 minutes.
26 different genres were used to describe the tv shows. The most common are comedy (1041), drama (637), reality tv (500), animation (390), and family (307). The least common are short (2), war (8), western (9), biography (13), and musical (14).
Some of the most common keywords are: relationships or relationship (755), female (298), family (284), father (250), sitcom (244).
There are no significant correlations among the features that are in their final form.
