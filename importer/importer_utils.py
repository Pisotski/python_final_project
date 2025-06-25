import logging
from query.query import get_player_id_by_name
from constants.name_corrections import NAME_CORRECTIONS


def normalize_name(name):
    name = name.strip()
    return NAME_CORRECTIONS[name] if name in NAME_CORRECTIONS else name


def enrich_review_with_player_id(df, conn):
    player_ids = []
    updated_names = []

    for name in df["Name(s)"]:
        stripped_name = name.strip()
        clean_name = NAME_CORRECTIONS.get(stripped_name, stripped_name)
        player_id = get_player_id_by_name(conn, clean_name)

        if player_id is None:
            logging.warning(f"No player found with name: {clean_name}")

        updated_names.append(clean_name if clean_name != stripped_name else name)
        player_ids.append(player_id)

    df["Name(s)"] = updated_names
    df["player_id"] = player_ids
    return df


# LIST OF PLAYERS THAT CAN'T BE LOCATED BY REGULAR SEARCH
# WARNING:root:No player found with name: Ty Cobb *
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: BobbyVeach
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: BobbyVeach
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Henie Manush
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Dale Alexander *
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Luis Aparacio
# WARNING:root:No player found with name: Luis Aparacio
# WARNING:root:No player found with name: Luis Aparacio
# WARNING:root:No player found with name: Luis Aparacio
# WARNING:root:No player found with name: Luis Aparacio
# WARNING:root:No player found with name: Billy North
# WARNING:root:No player found with name: Billy North
# WARNING:root:No player found with name: Cal Ripken, Jr.
# WARNING:root:No player found with name: Cal Ripken, Jr.
# WARNING:root:No player found with name: Cal Ripken, Jr.
# WARNING:root:No player found with name: Cal Ripken, Jr.
# WARNING:root:No player found with name: Ken Griffey, Jr.
# WARNING:root:No player found with name: Ken Griffey, Jr.
# WARNING:root:No player found with name: Ken Griffey, Jr.
# WARNING:root:No player found with name: Ken Griffey, Jr.
# WARNING:root:No player found with name: Ken Griffey, Jr.
# WARNING:root:No player found with name: Ken Griffey, Jr.
# WARNING:root:No player found with name: Ken Griffey, Jr.
# WARNING:root:No player found with name: Ken Griffey, Jr.
# WARNING:root:No player found with name: Ken Griffey, Jr.
# WARNING:root:No player found with name: Roberto Alomar
# WARNING:root:No player found with name: DustinPedroia
# WARNING:root:No player found with name: Adrian Beltre
# WARNING:root:No player found with name: Adrian Beltre
# WARNING:root:No player found with name: Jose Abreu
# WARNING:root:No player found with name: Jose Abreu
# WARNING:root:No player found with name: Jose Abreu
# WARNING:root:No player found with name: Jose Abreu
# WARNING:root:No player found with name: Jose Abreu
# WARNING:root:No player found with name: Jose Abreu
# WARNING:root:No player found with name: Jose Abreu
# WARNING:root:No player found with name: Jose Caballero
# [SUCCESS] Inserted 1476 rows into 'player_review'.
# WARNING:root:No player found with name: Smoky Joe Wood
# WARNING:root:No player found with name: Smoky Joe Wood
# WARNING:root:No player found with name: Smoky Joe Wood
# WARNING:root:No player found with name: Smoky Joe Wood
# WARNING:root:No player found with name: Smoky Joe Wood
# WARNING:root:No player found with name: Smoky Joe Wood
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Babe Ruth
# WARNING:root:No player found with name: Allan Russell
# WARNING:root:No player found with name: Joe Bush
# WARNING:root:No player found with name: Allan Russell
# WARNING:root:No player found with name: Hod Lisenbee
# WARNING:root:No player found with name: Al Worthington
# WARNING:root:No player found with name: La Marr Hoyt
# WARNING:root:No player found with name: La Marr Hoyt
# WARNING:root:No player found with name: Mark Eichhorn
# WARNING:root:No player found with name: Bob Wickman
# WARNING:root:No player found with name: Bob Wickman
# WARNING:root:No player found with name: C.C. Sabathia
# WARNING:root:No player found with name: Felix Hernandez
# WARNING:root:No player found with name: Felix Hernandez
# WARNING:root:No player found with name: Felix Hernandez
# WARNING:root:No player found with name: C.C. Sabathia
# WARNING:root:No player found with name: Felix Hernandez
# WARNING:root:No player found with name: Anibal Sanchez
# WARNING:root:No player found with name: Felix Hernandez
# WARNING:root:No player found with name: Zach Britton
# WARNING:root:No player found with name: Alex Colome
# WARNING:root:No player found with name: Jose Berrios
# WARNING:root:No player found with name: Jose Berrios
# WARNING:root:No player found with name: Yusmeiro Petit
# WARNING:root:No player found with name: Lance McCullers, Jr.
# [SUCCESS] Inserted 1025 rows into 'pitcher_review'.

# Scrape individually:
# https://www.baseball-almanac.com/players/player.php?p=griffke02
# https://www.baseball-almanac.com/players/player.php?p=aparilu01
# https://www.baseball-almanac.com/players/player.php?p=alomaro01
# https://www.baseball-almanac.com/players/player.php?p=worthal01
# https://www.baseball-almanac.com/players/player.php?p=ruthba01
# https://www.baseball-almanac.com/players/player.php?p=eichhma01
# https://www.baseball-almanac.com/players/player.php?p=wickmbo01
# https://www.baseball-almanac.com/players/player.php?p=petityu01
