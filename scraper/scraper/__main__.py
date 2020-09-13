from scraper.scrape import run
from scraper.api import DataAPI
import time


def main():
    """The main routine."""
    try:
        time.sleep(5)
        api = DataAPI()
        if len(api.categories) and len(api.tags) and api.test_geo():
            api.logout()
            run()
    except Exception as e:
        print(f"Error: {e}. \n\n Sleeping 60 seconds...")
        time.sleep(60)


if __name__ == '__main__':
    main()
