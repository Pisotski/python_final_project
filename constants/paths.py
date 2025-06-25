import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

BASE_URL = "https://www.baseball-almanac.com/"
CSV_PATH = os.path.join(PROJECT_ROOT, "data", "raw", "players.csv")
CSV_PATH_PLAYER_REVIEW = os.path.join(PROJECT_ROOT, "data", "raw", "player_review.csv")
CSV_PATH_PITCHER_REVIEW = os.path.join(
    PROJECT_ROOT, "data", "raw", "pitcher_review.csv"
)
DB_PATH = "data/mlb_players.db"
LOG_PATH = os.path.join(PROJECT_ROOT, "last_link", "last_link_history.txt")
