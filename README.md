# Internship Scraper
### This application runs daily at 8AM via CRONJOB and does the following
### 1. Scrapes the webpage - https://github.com/pittcsc/Summer2022-Internships
#### Thank you to the students who maintain this repo!!
### 2. Checks to see if there are any new postings, if so it adds it to the DynamoDB that is set up (AWS Free Tier)
### 3. If there are new postings, it sends those results to the slack bot and then posts to a channel with the new results
### 4. If no other new postings - sends the message that there are no new postings.


### Resources
#### Summer Internships - https://github.com/pittcsc/Summer2022-Internships
#### Slack API - https://api.slack.com/legacy/custom-integrations
#### AWS DynamoDB - https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
