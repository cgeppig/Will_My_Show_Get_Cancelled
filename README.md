# DSI_Capstone

# Will My Show Get Cancelled?

### By Chris Eppig, Ph.D.


## 1) The Problem

Dozens of new TV shows are released every season. Many of these shows succeed, but many are quickly cancelled due to low viewer interest. Production studios spend millions of dollars producing and marketing new shows, and this money may be lost if the show fails to generate sufficient advertising revenue.

Television viewers may become invested in a new show, only to be disappointed when it comes to an early end. Having advance warning of a show's fate will not prevent cancellation, but it can help prepare viewers for the outcome.

## 2) The Solution

In this analysis, a model was be created to predict whether a TV show will be cancelled in its first season. Success was determined by whether the model predicts cancellation better than chance.

The goal of this model was to make the most accurate predictions possible--being able to determine the impact of each variable was not a primary concern.

## 3) Data Collection and Cleaning

The titles of 2935 American TV shows from between 1980 and 2015 were taken from a Wikipedia entry: https://en.wikipedia.org/wiki/List_of_American_Television_programs_by_date

Shows from prior to 1980 were not included because of an expectation of poor data quality. Shows from 2016 were not included because they may not have been on the air for long enough for a cancellation/renewal decision to be made by the network. Only American shows were used because of the possibility that foreign shows would introduce too many additional variables.

Beyond the show titles, data was obtained from [the Internet Movie Database](http://www.imdb.com/) (IMDB) API, [OMDbAPI](http://www.omdbapi.com). Through this API, a function was used to search for each show title and cycle through the results until one was found that was a TV show, as opposed to the other forms of media included on the IMDB, which may include TV shows and movies with the same or similar names (e.g. [Limitless](http://www.imdb.com/title/tt1219289/?ref_=nv_sr_2) (2011) and [Limitless](http://www.imdb.com/title/tt4422836/?ref_=nv_sr_1) (2015)). The important information that this function retrieved was the unique identifier that IMDB uses for each item in its database (IMDB ID). Using this identifier, another function retrieved all of the information from the API, including plot description, parental ratings, genre, release data, runtime, and the number of seasons for which the show ran.

Plot keywords and distribution network were scraped directly from the IMDB website.

Of the original 2935 shows, 2016 were used in the final analysis. 874 shows were not used because important data was missing.

## 4) Features

Shows were considered to be cancelled if the number of seasons listed on IMDB was 1. Although most shows are cancelled eventually, this analysis was to predict whether they would be cancelled in one season. For stakeholders in the television industry, this predicts shows that are never profitable enough to be renewed.

Most television networks have half hour and full hour time slots for shows. Because of commercial breaks, the actual run time of an episode is less than the duration of the time slot. Two features were created for run time: "half_hour" was defined as length >= 20 minutes AND length <= 30 minutes. "full_hour" was defined as length >= 40 minutes AND length <= 60 minutes.

IMDB identifies 24 genres for TV shows: action, adventure, animation, biography, documentary, drama, family, fantasy, sci-fi, game show, history, horror, music, musical, mystery, news, reality TV, romance, short, sport, talk, thriller, war, and western. These were extracted using count vectorizer, and then converted into dummy variables.

Keywords on IMDB are much more variable than genres. They can be a single word (e.g. "mythology," "friendship" or "space"), or multiple words (e.g. "brother sister relationship" or "workplace romance"). Sometimes multiple keywords refer to the same thing (e.g. "based on comic book" and "based on comic" or "friend" and "friendship"). In other cases, there are closely related groups of keywords, such as those describing relationships (e.g. "brother sister relationship," "father daughter relationship" or "husband wife relationship"). Simply using all of the most common keywords as listed would either produce an unwieldy number of features, or fail to capture sufficient variance. To solve this problem, all of the keywords were stemmed, and count vectorizer was used to extract the 100 most common words. Of these top 100 keywords, terms were removed if they referred to a date (e.g. "1990s" or "2000s"), or if they had no important content (e.g. "ex" or "TV"). Dummy variables were produced for each of the remaining 83 keywords.

Distribution networks were not listed consistently on IMDB. For example, CBS could be listed as "CBS Television Network" or as "Columbia Broadcasting System (CBS)." For the 11 most common networks (ABC, NBC, CBS, Fox, Nickelodeon, Cartoon Network, Comedy Central, MTV, HBO, Disney, and WB), dummy variables were created based on whether certain strings were present that could uniquely identify a network (e.g. "CBS" or "NBC").

The date on which the first episode of a show aired was retrieved from the API in string format. This was converted into a datetime object, which allowed the extraction of date-related information. Release year and day of the month were added as numerical features. Month and day of the week were added as dummy variables.

A total of 142 features were created within these five categories.

## 5) Exploratory Data Analysis

The most common years of release within this data set was 2007-2010. This does not necessarily reflect a high point in the number of shows released, but likely reflects the available data. Although this data set originally included shows dating back to 1980, most shows from the 1980s were absent from the cleaned data.

![](https://github.com/cgeppig/DSI_Capstone/blob/master/figures/yearly.png)

The networks that released the most number of shows (ABC, NBC, CBS, and Fox) also cancelled the highest proportion of those shows, with each of these networks cancelling approximately half of their new shows within the first season. The networks cancelling the fewest proportion of their new shows were Nickelodeon, Cartoon Network and HBO.

![](https://github.com/cgeppig/DSI_Capstone/blob/master/figures/networks.png)

New shows are most likely to be released on Sunday and Monday, and on the first day of the month. By a wide margin, the most popular release month is September, followed distantly by October and January. Half-hour shows are slightly less likely to be cancelled than full-hour shows (35% vs 40%, respectively).

![](https://github.com/cgeppig/DSI_Capstone/blob/master/figures/weekdays.png)

![](https://github.com/cgeppig/DSI_Capstone/blob/master/figures/month.png)


## 6) Modeling

The cleaned data set was divided into training and test subsets--the training set contained 1545 rows, and the test set contained 516 rows. 39% of the shows in the final data set were cancelled; thus the base probability for this model was 0.39.

AdaBoost classifier was used to predict cancellation or renewal. Other modeling techniques, such as random forest, produced similar accuracy scores, but over-predicted renewal. AdaBoost was accurate at producing both renewal and cancellation, and had a balanced number of false positives and false negatives. Using 100 estimators, the model accuracy was 0.73 on the training set and 0.68 on the test set.

![](https://github.com/cgeppig/DSI_Capstone/blob/master/figures/classification_report.png)

![](https://github.com/cgeppig/DSI_Capstone/blob/master/figures/confusion_matrix.png)

![](https://github.com/cgeppig/DSI_Capstone/blob/master/figures/adaboost_roc.png)


## 7) Conclusions

With a base probability of 0.39 and a model accuracy of 0.68, this model performs significantly better than chance. False negatives and false positives are balanced.

From an industry perspective, the information produced by this model is actionable. By manipulating the variables in the model, it would be possible to create show outlines and release dates that would have a higher chance of success. The only variable that is not possible to directly manipulate is release year, but the information gained by it is still actionable. By keeping the year constant (presumably the current year), this model is able to determine what genres and other features are likely to be successful in that year.

## 8) Future Directions

This model could be improved by the addition of a variety of features.

Some TV shows are based on movies or other TV shows (e.g. [Limitless](http://www.imdb.com/title/tt4422836/?ref_=nv_sr_1) and most of the Star Trek franchise), which attempt to ride the popularity of the preceding material. Spinoff shows may have a higher or lower rate of cancellation than completely original shows. Likewise, some shows have actors, directors, writers, or producers who are particularly famous, or who have been involved in other popular works, and this may influence the show's success. For example, [Joss Whedon](http://www.imdb.com/name/nm0923736/?ref_=nv_sr_1) has a history of creating shows with loyal followings (e.g. [Buffy the Vampire Slayer](http://www.imdb.com/title/tt0118276/?ref_=nv_sr_1) and [Firefly](http://www.imdb.com/title/tt0303461/?ref_=nv_sr_1))--his 2009 show [Dollhouse](http://www.imdb.com/title/tt1135300/?ref_=nv_sr_1), which lasted for 2 seasons, may have been cancelled sooner if not for his involvement.

The features of the central cast may also play a role. Shows with a single main character may perform differently than an ensemble cast. The age, race and sex of the central cast members may also be important.

Production and advertising budget could influence a show's success in a variety of ways. A show with a higher budget may be of higher quality, and therefore attract and keep more viewers. Studios that spend a lot of money on a show may be more reluctant to cancel it (i.e. the Concorde Fallacy). Conversely, a studio that spends a lot of money on a show may be more willing to cut their losses if the show is not performing well.

Parental ratings affect the size of a show's potential audience. A show that is suitable for viewers of all ages has a higher potential for a large audience size and associated advertising revenue. However, shows that are more targeted to specific audiences--such as adults--may have greater success in attracting and keeping viewers. The main problem with using this data is that parental ratings for TV shows have not been in use or in a standard format for as long as MPAA ratings have been for movies. Thus, the available data is sparse and inconsistent.

Future iterations of this model will attempt to include these features.
