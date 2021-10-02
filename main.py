from scraper import Scraper
from slack_bot import send_results
import json


def main():
    scraper = Scraper()
    send_results("Starting Scraper...")
    response = scraper.get_url()
    postings = scraper.start_scraper(response)
    # print(scraper.create_table("internships_swe","Company"))
    table = scraper.connect_to_db_table("internships_swe")
    print(scraper.check_size_of_table(table))
    new_items = scraper.check_for_duplicates(table, postings)
    print(scraper.add_records(table, new_items))
    send_results("Finished scraping, here's the new results...")
    send_results(json.dumps(new_items,indent=4))
    scraper.driver.quit()


if __name__ == "__main__":
    main()