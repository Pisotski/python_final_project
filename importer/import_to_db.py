import sqlite3
import csv
import os


def push_csv_to_sqlite(csv_path: str, db_path: str = "players.db"):
    if not os.path.exists(csv_path):
        print(f"[ERROR] File not found: {csv_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS players (
        player_name TEXT,
        year TEXT,
        team TEXT,
        league TEXT,
        position TEXT,
        age TEXT,
        games TEXT,
        batting_average TEXT,
        home_runs TEXT,
        rbi TEXT
    )
    """
    )

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [
            (
                row.get("player_name"),
                row.get("year"),
                row.get("team"),
                row.get("league"),
                row.get("position"),
                row.get("age"),
                row.get("games"),
                row.get("batting_average"),
                row.get("home_runs"),
                row.get("rbi"),
            )
            for row in reader
        ]

    cursor.executemany(
        """
        INSERT INTO players (
            player_name, year, team, league, position,
            age, games, batting_average, home_runs, rbi
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        rows,
    )

    conn.commit()
    conn.close()
    print(f"[SUCCESS] Inserted {len(rows)} rows into '{db_path}'.")
