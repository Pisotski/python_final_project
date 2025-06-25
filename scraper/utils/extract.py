from selenium.webdriver.common.by import By
from urllib.parse import urljoin
from .driver import get_driver
import time

BASE_URL = "https://www.baseball-almanac.com/"


def get_all_links():
    driver = get_driver()
    driver.get("https://www.baseball-almanac.com/yearmenu.shtml")
    time.sleep(2)
    rows = driver.find_elements(By.TAG_NAME, "tr")

    target_text = "The History of the American League From 1901 to 2025"
    target_index = next(
        i
        for i, row in enumerate(rows)
        if any(
            td.text.strip() == target_text
            for td in row.find_elements(By.TAG_NAME, "td")
        )
    )

    next_row = rows[target_index + 1]

    year_links_set = set()
    for td in next_row.find_elements(By.TAG_NAME, "td"):
        for a in td.find_elements(By.TAG_NAME, "a"):
            href = a.get_attribute("href")
            text = a.text.strip()
            if href and text.isdigit():
                year = int(text)
                full_link = urljoin(BASE_URL, href)
                year_links_set.add((year, full_link))

    return sorted(list(year_links_set))


def extract_links_for_players():
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

    seen = set()
    unique_links = []
    for link in raw_links:
        if link not in seen:
            seen.add(link)
            unique_links.append(link)
    return unique_links


def extract_day_page(driver, link):
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


def get_tables(url):
    driver = get_driver()
    driver.get(url)
    time.sleep(1.5)
    tables = driver.find_elements(By.CSS_SELECTOR, "div.ba-table table.boxed")
    return tables, driver


def extract_player_review_table(table_element, year):
    rows = table_element.find_elements(By.TAG_NAME, "tr")
    data = []

    for row in rows:
        if any(
            "banner" in cell.get_attribute("class").lower()
            or "header" in cell.get_attribute("class").lower()
            for cell in row.find_elements(By.TAG_NAME, "td")
        ):
            continue

        cells = row.find_elements(By.TAG_NAME, "td")
        try:
            name_cell = cells[1]
            link_element = name_cell.find_element(By.TAG_NAME, "a")
            player_link = link_element.get_attribute("href")
        except Exception:
            continue

        if len(cells) != 5:
            continue

        texts = [cell.text.strip() for cell in cells]
        if texts == ["Statistic", "Name(s)", "Team(s)", "#", "Top 25"]:
            continue

        stat = texts[0]
        name = texts[1]
        team = texts[2]
        value = texts[3]

        if name == "To Be Determined":
            continue

        dob = get_dob_from_player_page(player_link)

        data.append(
            {
                "Year": year,
                "Statistic": stat,
                "Name(s)": name,
                "Team(s)": team,
                "#": value,
                "Date of Birth": dob,
            }
        )

    return data


def extract_pitcher_review_table(table_element, year):
    rows = table_element.find_elements(By.TAG_NAME, "tr")
    data = []

    current_stat = None
    current_value = None

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")

        if not cells or any(
            "banner" in c.get_attribute("class").lower()
            or "header" in c.get_attribute("class").lower()
            for c in cells
        ):
            continue

        texts = [cell.text.strip() for cell in cells]

        if len(cells) == 5:
            stat, name, team, value, _ = texts

            if name == "To Be Determined":
                continue

            try:
                name_cell = cells[1]
                link_element = name_cell.find_element(By.TAG_NAME, "a")
                player_link = link_element.get_attribute("href")
                dob = get_dob_from_player_page(player_link)
            except Exception:
                dob = None

            data.append(
                {
                    "Year": year,
                    "Statistic": stat,
                    "Name(s)": name,
                    "Team(s)": team,
                    "#": value,
                    "Date of Birth": dob,
                }
            )

            current_stat = stat
            current_value = value

        elif len(cells) == 3:
            name, team = texts[0], texts[1]

            if name == "To Be Determined":
                continue

            try:
                name_cell = cells[0]
                link_element = name_cell.find_element(By.TAG_NAME, "a")
                player_link = link_element.get_attribute("href")
                dob = get_dob_from_player_page(player_link)
            except Exception:
                dob = None

            data.append(
                {
                    "Year": year,
                    "Statistic": current_stat,
                    "Name(s)": name,
                    "Team(s)": team,
                    "#": current_value,
                    "Date of Birth": dob,
                }
            )

    return data


def get_dob_from_player_page(player_url):
    print(f"[INFO] Extracting {player_url}")
    try:
        driver = get_driver()
        driver.get(player_url)
        time.sleep(1.2)

        bio_table = driver.find_element(By.CLASS_NAME, "ba-table")
        inner_table = bio_table.find_element(By.XPATH, './/td[@width="50%"]/table')
        rows = inner_table.find_elements(By.TAG_NAME, "tr")
        print(f"[DEBUG] Found {len(rows)} bio rows on {player_url}")

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 2:
                label = cells[0].text.strip().lower()
                if "born" in label:
                    dob = cells[1].text.strip()
                    print(f"[INFO] Got DOB for {label}: {dob}")
                    return dob

    except Exception as e:
        print(f"[ERROR] Could not get DOB from {player_url}: {e}")

    finally:
        driver.quit()

    return None
