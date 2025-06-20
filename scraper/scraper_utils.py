from selenium.webdriver.common.by import By


def parse_biography_table(biography_element):
    def clean(text):
        return text.strip().replace("\xa0", " ").rstrip(":") or "null"

    try:
        data_row = biography_element.find_element(
            By.CSS_SELECTOR, "table > tbody > tr:nth-child(4)"
        )
    except:
        print("Could not find the data row with biography tables.")
        return {}

    inner_tables = data_row.find_elements(By.CSS_SELECTOR, "td > table")
    if not inner_tables:
        print("No inner tables found in the data row.")
        return {}

    biography_data = {}

    for table in inner_tables:
        rows = table.find_elements(By.CSS_SELECTOR, "tbody > tr")

        for tr in rows:
            tds = tr.find_elements(By.TAG_NAME, "td")
            td_count = len(tds)

            if td_count == 2:
                key = clean(tds[0].text)
                value = clean(tds[1].text)
                if value.lower() in {"n/a", "na", "none"}:
                    value = "null"
                biography_data[key] = value

            elif td_count == 5:
                key1 = clean(tds[0].text)
                value1 = clean(tds[1].text)
                key2 = clean(tds[3].text)
                value2 = clean(tds[4].text)

                if value1.lower() in {"n/a", "na", "none"}:
                    value1 = "null"
                if value2.lower() in {"n/a", "na", "none"}:
                    value2 = "null"

                biography_data[key1] = value1
                biography_data[key2] = value2

            elif td_count >= 2:
                key = clean(tds[0].text)
                value = clean(" ".join(td.text for td in tds[1:]))
                if value.lower() in {"n/a", "na", "none"}:
                    value = "null"
                biography_data[key] = value

            else:
                print(f"Skipping unexpected td count: {td_count}")

    return biography_data
