import sqlite3

from constants.paths import DB_PATH


def get_player_id_by_name(conn, name):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM players WHERE `Full Name` = ?", (name,))
    result = cursor.fetchone()
    return result[0] if result else None


def query_players_by_year(year):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        query = """
        SELECT `Name(s)`, Statistic, `#`
        FROM player_review
        WHERE Year = ?
        ORDER BY Statistic, `Name(s)`
        LIMIT 10;
        """
        cursor.execute(query, (year,))
        rows = cursor.fetchall()
    return rows


def query_player_info(player_name):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        query = """
        SELECT 
            "Birth Name", "Nickname", "Date of Birth", "Birth City",
            "Date of Death", "Death City", "Cemetery", "High School",
            "College", "Bats", "Throws", "Height (ft-in)", "Weight",
            "First Game", "Last Game", "Zodiac Sign"
        FROM players
        WHERE "Full Name" = ?
        LIMIT 1;
        """
        cursor.execute(query, (player_name,))
        row = cursor.fetchone()
    return row
