import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import boto3
from boto3.dynamodb.conditions import Key
import json


"""
This will be the Scraper class that includes all of the functions from
scraping the webpage.
To CRUD functions for the DynamoDB
"""
class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.url = "https://github.com/pittcsc/Summer2022-Internships"
        self.posting = []
        self.links = []
        self.new_items = []

    """
    This function handles requesting the URL
    PARAMETERS:
        Nothing

    RETURNS:
        r: The response to use in other functions
        self.driver: the driver needed 
    """
    def get_url(self):
        print(f"The URL is {self.url}")
        self.driver.get(self.url)
        r = requests.get(self.url)
        if (r.status_code == 200):
            print(f"Request was sucessful. Response code was {r.status_code}")
            print(f"url used was {r.url}")
            return r
        else:
            return f"Error happended when trying to request {self.url}"

    """
    This functions handles the actual scraping portion.
    PARAMETERS:
        Response: The response that is returned from the "get_urL" function

    RETURNS:
        postings: A dictionary that holds all of the records to be updated
    """
    def start_scraper(self, response):
        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.find_all("table")[0]
        columns = ["Company","Location","Details","Link"]
        id = 0
        for row in tables.find_all("tr"):
            try:
                row_list = row.find_all(["th","td"])
                link = row_list[0].find("a")["href"]
                company = row_list[0].text
                location = row_list[1].text
                notes = row_list[2].text
                obj = {
                    "Id" : id,
                    "Company" : company,
                    "Location" : location,
                    "Notes" : notes,
                    "URL" : link
                }
                id += 1
                self.posting.append(obj)
            except Exception as e:
                print(f"Error occured. {e}")
        self.driver.quit()

        return self.posting

    """
    This functions handles connecting to the DynamoDB
    It prints out some basic information like table name, the created date, as well as the status
    
    PARAMETERS:
        table: this will be the table name to connect to

    RETURNS:
        table_db: table connection to reuse in other DB functions
    """
    def connect_to_db_table(self, table):
        dynamodb = boto3.resource("dynamodb")
        table_db = dynamodb.Table(table)
        if table_db is not None:
            print(f"Successfully connected to {table_db.name}!")
            print(f"The table was created on {table_db.creation_date_time.strftime('%Y-%m-%d')}")
            print(f"The table status is {table_db.table_status}")
            return table_db
        else:
            return f"Had some issues connecting to the DynamoDB table {table}..."

    """
    This functions returns the table schema.

    PARAMETERS:
        table: table connection to use to connect to the table
    
    RETURNS:
        Table schema of the table passed in
    """
    def get_table_schema(self, table):
        client = boto3.client("dynamodb")
        response = client.describe_table(TableName=table)
        return json.dumps(response, indent=4, default=str)

    """
    This function checks the size of the table

    PARAMETERS:
        table: table connection to use to connect to the table
    
    RETURNS:
        Current Size of the table in bytes
    """
    def check_size_of_table(self, table):
        if table is not None:
            return f"Size of the table is {table.table_size_bytes} in bytes"
        else:
            return f"{table} not found"

    """
    This function handles adding the records from our "postings"

    PARAMETERS:
        table: table connection to use
        postings: the dictionary object that holds all of the results from the scraper
    
    RETURNS:
        Nothing
    """
    def add_records(self, table, new_items):
        if len(self.new_items) == 0:
            return f"No new items to add, Moving on..."
        else:
            for record in self.new_items:
                item = {
                    "Id":record["Id"],
                    "Company":record["Company"],
                    "Location":record["Location"],
                    "Notes":record["Notes"],
                    "URL":record["URL"]
                }
                print(f"Now adding the item {item}")
                table.put_item(Item=item)
        return f"Finished updating the table {table.name}"

    """
    This functions handles querying the database for a specific record

    PARAMETERS:
        table: table connection to use
        record: key to search the db with, this is using the primary index (the "Id")
    
    RETURNS:
        response of the request. Returns "No record for {record} found" if response is invalid
            {record} -> is the record we're looking for
    """
    def query_records(self, table, record):
        response = table.get_item(
            Key={
                "Company":record
            }
        )
        try:
            if response["Item"] is not None:
                return response["Item"]
        except:
            return f"No record for {record} was found"

    """
    This function will check for duplicates in the current db
    We'll use the "id" here to check

    PARAMETERS:
        table: table connection to use
        postings: dictionary of the scraper results

    RETURNS:
        Success message if no duplicates
        If there are, return the duplicate we found
    """
    def check_for_duplicates(self, table, postings):
        print("Checking to see if there are any duplicates...")
        for posting in postings:
            response = table.get_item(
                Key={
                    "Company":posting["Company"]
                }
            )
            if "Item" in response:
                print(f"Item already is already in db. Moving on...")
            else:
                print(f"Item {posting} is new, adding to db")
                self.new_items.append(posting)
        if len(self.new_items) == 0:
            return "No new items to add today..."
        items_to_add = self.new_items
        return items_to_add

        


    """
    This function will handle deleting the table given.

    PARAMETERS:
        table: table connection to delete

    RETURNS:
        Success message that we deleted the table
    """
    def drop_table(self, table):
        client = boto3.client("dynamodb")
        response = client.delete_table(TableName=table.name)
        return f"We dropped table {table.name}. Response was \n{response}"


    def create_table(self, table, primary_key):
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.create_table(
            TableName=table,
            KeySchema=[
                {
                    "AttributeName": primary_key,
                    "KeyType":"HASH"
                }
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": primary_key,
                    "AttributeType":"S"
                }
            ],
            ProvisionedThroughput={
                    "ReadCapacityUnits":5,
                    "WriteCapacityUnits":5
                }
        )
        return f"Table {table} was created "