# %%
import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from scraper_utils import parse_biography_table
from urllib.parse import urljoin

# === CONFIG ===
RESTART_EVERY_N_LINKS = 5
WAIT_TIME = 1.5
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_PATH = os.path.join(PROJECT_ROOT, "data", "raw", "players.csv")
LOG_PATH = os.path.join(PROJECT_ROOT, "last_link.txt")


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    )


def get_all_links():
    driver = get_driver()
    driver.get("https://www.baseball-almanac.com")
    time.sleep(2)
    rows = driver.find_elements(By.TAG_NAME, "tr")

    banner_indices = [
        i
        for i, row in enumerate(rows)
        if any(
            "banner" in td.get_attribute("class")
            for td in row.find_elements(By.TAG_NAME, "td")
        )
    ]
    start_index = banner_indices[-2]
    current_row = rows[start_index].find_element(By.XPATH, "following-sibling::*[1]")

    raw_links = []
    for _ in range(6):
        tds = current_row.find_elements(By.TAG_NAME, "td")
        for td in tds:
            for link in td.find_elements(By.TAG_NAME, "a"):
                href = link.get_attribute("href")
                text = link.text.strip()
                if href and text:
                    full_link = urljoin("https://www.baseball-almanac.com", href)
                    raw_links.append(full_link)
        current_row = current_row.find_element(By.XPATH, "following-sibling::*[1]")
    driver.quit()

    # Remove duplicates, preserve order
    seen = set()
    unique_links = []
    for link in raw_links:
        if link not in seen:
            seen.add(link)
            unique_links.append(link)
    return unique_links


def load_last_link():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH) as f:
            return f.read().strip()
    return None


def save_last_link(link):
    with open(LOG_PATH, "w") as f:
        f.write(link)


def scrape_day_page(driver, link):
    driver.get(link)
    table = driver.find_element(By.CSS_SELECTOR, "div.ba-table > table > tbody")
    rows = table.find_elements(By.TAG_NAME, "tr")[2:]

    players_links = []
    for row in rows:
        if any(
            "banner" in td.get_attribute("class")
            for td in row.find_elements(By.TAG_NAME, "td")
        ):
            break
        tds = row.find_elements(By.TAG_NAME, "td")
        if len(tds) < 2:
            continue
        link_element = tds[1].find_element(By.TAG_NAME, "a")
        players_links.append(
            {
                "player_name": link_element.text.strip(),
                "player_url": link_element.get_attribute("href"),
            }
        )
    return players_links


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


# === MAIN LOOP ===
if __name__ == "__main__":

    all_links = get_all_links()
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
                    players = scrape_day_page(driver, link)
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
