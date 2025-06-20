import pandas as pd
import re


def extract_date_and_zodiac(value):
    if pd.isna(value):
        return (pd.NaT, pd.NA)

    match = re.match(r"(\d{2}-\d{2}-\d{4})\s+\((.*?)\)", str(value).strip())
    if match:
        date_part = match.group(1)
        zodiac = match.group(2)
    else:
        date_match = re.match(r"\d{2}-\d{2}-\d{4}", str(value))
        date_part = date_match.group(0) if date_match else None
        zodiac = pd.NA

    try:
        clean_date = pd.to_datetime(date_part, format="%m-%d-%Y", errors="coerce")
    except:
        clean_date = pd.NaT

    return clean_date, zodiac


def normalize_hand(val):
    if pd.isna(val):
        return pd.NA
    val = str(val).lower()
    if val.startswith("r"):
        return "Right"
    if val.startswith("l"):
        return "Left"
    if val.startswith("b"):
        return "Both"
    return pd.NA


def split_first_game(value):
    if pd.isna(value):
        return (pd.NaT, pd.NA)

    match = re.match(r"^([\d/-]+)\s*(?:\(Age\s*(\d+)\))?$", value.strip())
    if match:
        date_str = match.group(1).strip()
        age_str = match.group(2)
        date = pd.to_datetime(date_str, errors="coerce")
        age = int(age_str) if age_str is not None else pd.NA
        return (date, age)

    return (pd.NaT, pd.NA)


def split_location(value):
    if pd.isna(value) or "," not in value:
        return (pd.NA, pd.NA)

    parts = [part.strip() for part in value.split(",", 1)]
    if len(parts) == 2:
        return parts[0], parts[1]
    else:
        return parts[0], pd.NA


def split_school_and_location(value):
    if pd.isna(value):
        return (pd.NA, pd.NA, pd.NA)

    match = re.match(r"^(.*?)\s*\((.*?)\)$", value.strip())
    if match:
        school = match.group(1).strip()
        location = match.group(2).strip()
        if "," in location:
            city, state = [part.strip() for part in location.split(",", 1)]
        else:
            city, state = location, pd.NA
        return school, city, state
    else:
        return value.strip(), pd.NA, pd.NA


def parse_height(h):
    if pd.isna(h):
        return None

    try:
        h = h.replace("½", ".5").replace("¼", ".25").replace("¾", ".75")

        feet, inches = h.split("-")
        return int(feet) * 12 + float(inches)
    except Exception:
        return None
