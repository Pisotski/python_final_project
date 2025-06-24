import logging
from cli_query.query import get_player_id_by_name


def enrich_review_with_player_id(df, conn):
    player_ids = []
    for name in df["Name(s)"] if "Name(s)" in df.columns else df["Name"]:
        player_id = get_player_id_by_name(conn, name)
        if player_id is None:
            logging.warning(f"No player found with name: {name}")
        player_ids.append(player_id)
    df["player_id"] = player_ids
    return df
