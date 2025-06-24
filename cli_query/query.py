def get_player_id_by_name(conn, name):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM players WHERE `Full Name` = ?", (name,))
    result = cursor.fetchone()
    return result[0] if result else None
