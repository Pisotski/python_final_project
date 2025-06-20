import re


def height_string_to_inches(height_str):
    if not isinstance(height_str, str):
        return None

    match = re.match(r"^(\d+)-(\d+(?:\.\d+)?)$", height_str.strip())
    if match:
        feet = int(match.group(1))
        inches = float(match.group(2))
        return round(feet * 12 + inches, 1)

    return None
