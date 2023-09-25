# Final Project

## W205 Fall 2021

### Overview

This project uses the tools introduced in W205 - Fundamentals of Data Engineering to receive streaming data on tweets from twitter.com and uses it to perform analytics and generate interesting insights. The focus of the project is on tweet related to climate change and in particular this project aims to answer the following questions:

- What are the most frequently used words in the entire set of tweets?
- What are the frequently used words in the top 100 most retweeted tweets?
- What are the top 5 most active usernames?
- What are the top 5 most trending hastags?
- What are the top 10 most retweeted tweets?
- What fraction of retweets, likes and replies are from tweets with a URL in them, compared to tweets without a URL?
- What fraction of retweets, likes and replies are from tweets with a hashtag, compared to tweets without a hashtag?
- What percentage of tweets contain the hastags #happeningnow or #happening?

### Tools used

This project is completed entirely using the google cloud platform (GCP).The following tools are used as part of this project:

- Docker Compose: Used to create containers of various servies required to construct the data pipeline.
- Zookeeper: Used to track the status of nodes in the Kafka cluster and maintain a list of kafka topics and messages.
- Apache Kafka: Used as a broker to receive messages produced by a producer and store them in a topic.
- Spark: Used to consume messages stored in a Kafka topic, perform the requisite transformations and store them into HDFS as parquet files.
- HDFS: Distributed files sytem from Hadoop that is used to store the tweet data in temp tables.
- Presto: Used to query the tables stored in HDFS.

### Summary of results

The following are the insights generated through the analysis conducted in this project. A detailed discussion on the results can be found in the Final report Notebook.

- We see many interesting words in the wordcloud generated using the tweets. Words that mention actions that can mitigate the effects of climate change appear fairly frequently. Words that mention fossil fuels also appear, with somewhat lower frequency.
- The most common words used in the top 100 retweeted tweets seem to indicate concrete action on policies by government or other agencies.
- The most active twitter user accounts for ~0.007% of the tweets used in the analysis.
- Hashtags that aim to promote action about climate change appear more frequently than hashtags that aim to be  alarming.
- The most retweeted tweets are from public figures.
- Tweets without URLs and hashtags seem to be retweeted much more than tweets with URLs or hashtags. This may be because more tweets are created without URLs or hashtags.

### Description of the files

Following are the files requried to setup the data pipeline and perform the analysis on the data from twitter

- docker-compose.yml: This file contains the information requried for docker to setup up containers for all the differnet services.
- Stream_Filtered_Tweets_from_TwitterAPI.py: This file is used to connect to the twitter API using a authentication code provided by twitter. It also sets up the rules according to which the tweets are filterd and specifies the data fields that are requested from each tweet in the data stream. In addition, it sends the data from the twitter API stream to Kafka using a producer in binary format.
- ETL_withSpark_and_Write_to_Hadoop.py: This file creates a spark session that consumes messages stored in the Kafka producer. It converts the messages from binary format to string format, transforms the messages as requried and stores them into a table in HDFS.
- Querying_Data_using_Presto.ipynb: This notebook is used to query data from the tables stored in HDFS and perform analytics on the data.
- Final_Report.ipynb: This report describes the motivation and objective of this project. The data pipeline and the commands requried to set it up are explained. Results of queries and vizualizations created using those are provided and finally, the conclusions are reported.
- Readme.md - This file.
