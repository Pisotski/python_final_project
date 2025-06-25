import csv
import logging

from constants.paths import CSV_PATH
from scraper.utils.driver import get_driver
from scraper.utils.writer import write_players


players = [
    {
        "player_name": "Ken Griffey, Jr.",
        "player_url": "https://www.baseball-almanac.com/players/player.php?p=griffke02",
    },
    {
        "player_name": "Albert Pujols",
        "player_url": "https://www.baseball-almanac.com/players/player.php?p=aparilu01",
    },
    {
        "player_name": "Roberto Alomar",
        "player_url": "https://www.baseball-almanac.com/players/player.php?p=alomaro01",
    },
    {
        "player_name": "Al Worthington",
        "player_url": "https://www.baseball-almanac.com/players/player.php?p=worthal01",
    },
    {
        "player_name": "Babe Ruth",
        "player_url": "https://www.baseball-almanac.com/players/player.php?p=ruthba01",
    },
    {
        "player_name": "Mark Eichhorn",
        "player_url": "https://www.baseball-almanac.com/players/player.php?p=eichhma01",
    },
    {
        "player_name": "Bob Wickman",
        "player_url": "https://www.baseball-almanac.com/players/player.php?p=wickmbo01",
    },
    {
        "player_name": "Yusmeiro Petit",
        "player_url": "https://www.baseball-almanac.com/players/player.php?p=petityu01",
    },
]


def main():
    driver = get_driver()

    try:
        with open(CSV_PATH, mode="a", newline="", encoding="utf-8") as file:
            with open(CSV_PATH, mode="r", encoding="utf-8") as f_read:
                reader = csv.reader(f_read)
                headers = next(reader)

            writer = csv.DictWriter(file, fieldnames=headers)
            write_players(driver, players, writer)

    except Exception as e:
        logging.exception("Crashed while adding players")

    finally:
        driver.quit()
        print("Scraping complete.")


if __name__ == "__main__":
    main()
