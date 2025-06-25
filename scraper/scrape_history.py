import logging
from constants.paths import CSV_PATH_PITCHER_REVIEW, CSV_PATH_PLAYER_REVIEW
from scraper.utils.extract import (
    get_all_links,
    get_tables,
    extract_player_review_table,
    extract_pitcher_review_table,
)
from scraper.utils.writer import write_to_csv


def scrape_history():
    player_review_data = []
    pitcher_review_data = []

    all_links = get_all_links()
    selected_links = all_links

    #
    #   FOR TESTING:
    #   this will take 2 links for the head, 2 from the middle and 2 from the tails
    #   UNCOMMENT TO: double check how the entire process works. Scrapes data save to cvs's.
    #
    #   n = len(all_links)
    #   selected_links = all_links[:2] + all_links[n // 2 - 1 : n // 2 + 1] + all_links[-2:]
    #

    for year, link in selected_links:
        logging.info(f"Scraping year {year} from {link}")
        try:
            tables, driver = get_tables(link)
            if len(tables) < 3:
                logging.warning(f"No tables found for {year}")
                continue

            (
                player_review_table,
                pitcher_review,
                team_standings,
            ) = tables[:3]

            player_year_data = extract_player_review_table(player_review_table, year)
            pitcher_year_data = extract_pitcher_review_table(pitcher_review, year)
            player_review_data.extend(player_year_data)
            pitcher_review_data.extend(pitcher_year_data)
        except Exception as e:
            logging.error(f"Error scraping {year} from {link}: {e}")

        finally:
            if driver:
                driver.quit()
    write_to_csv(player_review_data, CSV_PATH_PLAYER_REVIEW)
    write_to_csv(pitcher_review_data, CSV_PATH_PITCHER_REVIEW)
