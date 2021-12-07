# Internship Scraper
## As of 12/06/21 - This project only runs locally - if there's enough requests / PRs to make this host this on a server and making it accessible on different slack applications, I can work on that. Please submit a PR if interested!<br>
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

#### This is what it'll look like when adding new records
![image](https://user-images.githubusercontent.com/55965440/135736716-1aa0b39c-6c2c-407f-a9ee-0a81bafe7f10.png)

#### vs. when there are no new records to add
![image](https://user-images.githubusercontent.com/55965440/135736724-a9c9d668-75fa-46d9-b081-90a2c7f0faf3.png)

