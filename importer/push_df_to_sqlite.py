import sqlite3


def push_df_to_sqlite(df, db_path, table_name):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        columns = [
            f'"{col}" TEXT' if col != "player_id" else '"player_id" INTEGER'
            for col in df.columns
        ]
        columns_sql = ", ".join(columns)

        cursor.execute(
            f"""
            CREATE TABLE {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {columns_sql},
                FOREIGN KEY(player_id) REFERENCES players(id)
            )
        """
        )

        df.to_sql(table_name, conn, if_exists="append", index=False)

        print(f"[SUCCESS] Inserted {len(df)} rows into '{table_name}'.")

    except Exception as e:
        print(f"[ERROR] Failed to insert into {table_name}: {e}")
    finally:
        conn.close()


def push_players_to_sqlite(df, db_path, table_name):
    df = df.drop_duplicates()
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        cursor.execute(
            f"""
            CREATE TABLE {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                "Full Name" TEXT NOT NULL,
                "Birth Name" TEXT,
                "Nickname" TEXT,
                "Date of Birth" DATE NOT NULL,
                "Birth City" TEXT,
                "Birth State" TEXT,
                "Date of Death" DATE,
                "Death City" TEXT,
                "Death State" TEXT,
                "Cemetery" TEXT,
                "Zodiac Sign" TEXT,
                "High School Name" TEXT,
                "High School City" TEXT,
                "High School State" TEXT,
                "College" TEXT,
                "Draft Info" TEXT,
                "Bats" TEXT,
                "Throws" TEXT,
                "Height (ft-in)" TEXT,
                "Height (inches)" INTEGER,
                "Weight (lbs)" INTEGER,
                "First Game" TEXT,
                "First Game Age" TEXT,
                "First Game Date" DATE,
                "Last Game" DATE,
                UNIQUE("Full Name", "Date of Birth")
            )
        """
        )

        df.to_sql(table_name, conn, if_exists="append", index=False)

        print(
            f"[SUCCESS] Inserted {len(df)} rows into '{db_path}' table '{table_name}' with primary key."
        )

    except Exception as e:
        print(f"[ERROR] Failed to insert DataFrame into database: {e}")
    finally:
        conn.close()
