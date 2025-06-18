# %%
import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from scraper_utils import parse_biography_table

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()), options=options
)

# 1. Get to the player index page
url = "https://www.baseball-almanac.com"
driver.get(url)
time.sleep(2)

rows = driver.find_elements(By.TAG_NAME, "tr")

banner_indices = []
for i, row in enumerate(rows):
    tds = row.find_elements(By.TAG_NAME, "td")
    for td in tds:
        if "banner" in td.get_attribute("class"):
            banner_indices.append(i)
            break

start_index = banner_indices[-2]
links = []
next_sibling = rows[start_index].find_element(By.XPATH, "following-sibling::*[1]")

while next_sibling:
    try:
        link_elem = next_sibling.find_element(By.TAG_NAME, "a")
        link_href = link_elem.get_attribute("href")
        link_text = link_elem.text.strip()
        links.append((link_href, link_text))
        next_sibling = next_sibling.find_element(By.XPATH, "following-sibling::*[1]")
    except Exception:
        break

# 2. Visit first alphabetical index (e.g., "A")
driver.get(links[0][0])
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

    name_td = tds[1]
    link_element = name_td.find_element(By.TAG_NAME, "a")
    player_name = link_element.text.strip()
    player_url = link_element.get_attribute("href")
    players_links.append({"player_name": player_name, "player_url": player_url})

# 3. Set up CSV file
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
csv_path = os.path.join(project_root, "data", "raw", "players.csv")
file_exists = os.path.isfile(csv_path)

# 4. Loop through each player and scrape their data
with open(csv_path, mode="a", newline="", encoding="utf-8") as file:
    writer = None

    for player in players_links:
        try:
            driver.get(player["player_url"])
            time.sleep(1.5)

            tables = driver.find_elements(By.CSS_SELECTOR, "div.ba-table")
            if not tables:
                print(f"No tables found for {player['player_name']}")
                continue

            biography = tables[0]
            bio_dict = dict(parse_biography_table(biography))
            bio_dict["Player Name"] = player["player_name"]

            if writer is None:
                fieldnames = list(bio_dict.keys())
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()

            writer.writerow(bio_dict)
            print(f"Saved: {player['player_name']}")

        except Exception as e:
            print(f"Failed to scrape {player['player_name']}: {e}")

driver.quit()

# %%
