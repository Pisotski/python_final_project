import csv
import time
from constants.config import WAIT_TIME
from scraper.utils.misc import parse_biography_table
from selenium.webdriver.common.by import By


def write_to_csv(all_data, filename):
    if not all_data:
        return

    fieldnames = list(all_data[0].keys())

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_data)


def write_players(driver, players_links, writer):
    for player in players_links:
        try:
            driver.get(player["player_url"])
            time.sleep(WAIT_TIME)

            tables = driver.find_elements(By.CSS_SELECTOR, "div.ba-table")
            if not tables:
                print(f"No tables for {player['player_name']}")
                continue

            try:
                bio_dict = dict(parse_biography_table(tables[0]))
            except Exception as e:
                print(f"Failed parsing bio table for {player['player_name']}: {e}")
                continue
            bio_dict["Player Name"] = player["player_name"]
            writer.writerow(bio_dict)
            print(f"Saved: {player['player_name']}")
        except Exception as e:
            print(f"Failed to scrape {player['player_name']}: {e}")
