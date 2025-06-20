import sqlite3


def push_df_to_sqlite(df, db_path, table_name):
    try:
        conn = sqlite3.connect(db_path)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(
            f"[SUCCESS] Inserted {len(df)} rows into '{db_path}' table '{table_name}'."
        )
    except Exception as e:
        print(f"[ERROR] Failed to insert DataFrame into database: {e}")
    finally:
        conn.close()
