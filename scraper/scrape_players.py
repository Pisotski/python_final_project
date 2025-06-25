import os
import time
import csv

from selenium.webdriver.common.by import By
from constants.config import WAIT_TIME
from scraper.utils.driver import get_driver
from scraper.utils.extract import extract_day_page, extract_links_for_players
from scraper.utils.misc import parse_biography_table
from scraper.utils.writer import write_players

# === CONFIG ===
RESTART_EVERY_N_LINKS = 5
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_PATH = os.path.join(PROJECT_ROOT, "data", "raw", "players.csv")
LOG_PATH = os.path.join(PROJECT_ROOT, "last_link.txt")


def load_last_link():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH) as f:
            return f.read().strip()
    return None


def save_last_link(link):
    with open(LOG_PATH, "w") as f:
        f.write(link)


# === MAIN LOOP ===
if __name__ == "__main__":

    all_links = extract_links_for_players()
    last_link = load_last_link()

    if last_link in all_links:
        all_links = all_links[all_links.index(last_link) + 1 :]
    try:
        driver = get_driver()
        file_exists = os.path.isfile(CSV_PATH)

        with open(CSV_PATH, mode="a", newline="", encoding="utf-8") as file:
            writer = None

            for i, link in enumerate(all_links):
                try:
                    print(f"Processing {link} ({i + 1}/{len(all_links)})")
                    players = extract_day_page(driver, link)
                    time.sleep(WAIT_TIME)
                    if not writer and players:
                        driver.get(players[0]["player_url"])
                        time.sleep(WAIT_TIME)
                        tables = driver.find_elements(By.CSS_SELECTOR, "div.ba-table")
                        sample_dict = dict(parse_biography_table(tables[0]))
                        sample_dict["Player Name"] = players[0]["player_name"]
                        writer = csv.DictWriter(
                            file, fieldnames=list(sample_dict.keys())
                        )
                        if not file_exists:
                            writer.writeheader()

                    write_players(driver, players, writer)
                    save_last_link(link)

                    if (i + 1) % RESTART_EVERY_N_LINKS == 0:
                        driver.quit()
                        driver = get_driver()

                except Exception as e:
                    print(f"Crash on {link}: {e}")
                    # Recover from ChromeDriver crash
                    try:
                        driver.quit()
                    except:
                        pass
                    driver = get_driver()
                    continue
    finally:
        driver.quit()
        print("Scraping complete.")
