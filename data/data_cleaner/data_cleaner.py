import pandas as pd
from data.data_cleaner.data_cleaner_utils import (
    extract_date_and_zodiac,
    normalize_hand,
    split_first_game,
    split_location,
    split_school_and_location,
    parse_height,
)


def load_and_clean(csv_path):
    df = pd.read_csv(csv_path)

    df["Height (inches)"] = df["Height"].apply(parse_height)
    df["Weight"] = pd.to_numeric(df["Weight"], errors="coerce")
    df.replace(
        [
            "null",
            "Null",
            "None",
            "",
            " ",
            "Unknown",
            "Undetermined",
            "Not Applicable",
            "Not Yet Determined",
            "None Attended",
            "Cremated",
        ],
        pd.NA,
        inplace=True,
    )
    born_results = df["Born On"].apply(extract_date_and_zodiac)
    df["Born On"] = born_results.apply(lambda x: x[0])
    df["Born On"] = pd.to_datetime(
        df["Born On"], format="%m-%d-%Y", errors="coerce"
    ).dt.date
    df["Died On"] = df["Died On"].str.replace(r"\s*\(.*?\)", "", regex=True).str.strip()
    df["Died On"] = pd.to_datetime(
        df["Died On"], format="%m-%d-%Y", errors="coerce"
    ).dt.date
    df["Last Game"] = pd.to_datetime(df["Last Game"], errors="coerce").dt.date
    df["Zodiac Sign"] = born_results.apply(lambda x: x[1])
    df["Throws"] = df["Throws"].apply(normalize_hand)
    df["Bats"] = df["Bats"].apply(normalize_hand)
    df[["First Game Date", "First Game Age"]] = (
        df["First Game"].apply(split_first_game).apply(pd.Series)
    )
    df["First Game Date"] = pd.to_datetime(
        df["First Game Date"], errors="coerce"
    ).dt.date
    df[["Birth City", "Birth State"]] = (
        df["Born In"].apply(split_location).apply(pd.Series)
    )
    df[["Death City", "Death State"]] = (
        df["Died In"].apply(split_location).apply(pd.Series)
    )
    df[["High School", "High School City", "High School State"]] = (
        df["High School"].apply(split_school_and_location).apply(pd.Series)
    )

    df.rename(
        columns={
            "Player Name": "Full Name",
            "Born On": "Date of Birth",
            "Died On": "Date of Death",
            "High School": "High School Name",
            "Height": "Height (ft-in)",
            "Weight": "Weight (lbs)",
            "Draft": "Draft Info",
        },
        inplace=True,
    )

    column_order = [
        "Full Name",
        "Birth Name",
        "Nickname",
        "Date of Birth",
        "Birth City",
        "Birth State",
        "Date of Death",
        "Death City",
        "Death State",
        "Cemetery",
        "Zodiac Sign",
        "High School Name",
        "High School City",
        "High School State",
        "College",
        "Draft Info",
        "Bats",
        "Throws",
        "Height (ft-in)",
        "Height (inches)",
        "Weight (lbs)",
        "First Game",
        "First Game Age",
        "First Game Date",
        "Last Game",
    ]
    df = df[column_order]
    df.to_csv("data/clean/players_clean.csv", index=False)
    return df
