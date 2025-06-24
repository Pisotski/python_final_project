from scraper.scrape_history import scrape_history
from scraper.utils.logger import setup_logger


if __name__ == "__main__":
    setup_logger()
    scrape_history()
