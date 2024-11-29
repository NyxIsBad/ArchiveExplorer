from bs4 import BeautifulSoup
import csv
import requests
import regex as re

def get_html(url, output_file):
    # Download html file from url
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("HTML file downloaded successfully")
        with open(output_file, mode="w", encoding="utf-8") as file:
            file.write(response.text)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading HTML file: {e}")
        return None
    
def sum_sentences(a, b):
    # Extract the common part of the sentence (e.g., "Damage of Lightning Skills")
    match_a = re.match(r"([a-zA-Z\s]+)([+-]?\d+[%]?)(.*)", a)
    match_b = re.match(r"([a-zA-Z\s]+)([+-]?\d+[%]?)(.*)", b)

    if not match_a or not match_b:
        return "Invalid input format"

    # Extract the sentence and percentage values
    start_a, value_a, rest_a = match_a.groups()
    start_b, value_b, rest_b = match_b.groups()

    # Check if the part of the sentences match
    if start_a == start_b and rest_a == rest_b:
        # Sum the percentages
        if value_a[-1] == "%":
            value_a_int = int(value_a[:-1])
            value_b_int = int(value_b[:-1])
        else:
            value_a_int = int(value_a)
            value_b_int = int(value_b)
        total = value_a_int + value_b_int
        if total < 0:
            if value_a[-1] == "%":
                return f"{start_a}{total}%{rest_a}"
            else:
                return f"{start_a}{total}{rest_a}"
        else:
            if value_a[-1] == "%":
                return f"{start_a}+{total}%{rest_a}"
            else:
                return f"{start_a}+{total}{rest_a}"
    else:
        # Return both sentences if they don't match
        return f"{a}, {b}"

def parse(input_file, output_file, clean_file):
    with open(input_file, mode="r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Find the table with id="archive"
    table = soup.find("table", id="archive")

    # Extract data from each row
    rows = table.find("tbody").find_all("tr")
    data = []
    data_cleaned = []

    for row in rows:
        # Extract Eidolon Names
        eidolon_cells = row.find("td")
        eidolon_names = ",".join(
            [a["title"] for a in eidolon_cells.find_all("a", title=True)]
        )

        # Extract bonuses for each star level
        bonus_cell = row.find("td", class_="text-start")
        bonuses = [
            bonus.get_text(strip=True)
            for bonus in bonus_cell.find_all("div", class_="d-flex align-items-center my-1")
        ]
        # Remove the point "Eidolon Accumulated Points +\d+" from the bonuses
        bonuses = [re.sub(r"Eidolon Accumulated Points \+\d+", "", bonus) for bonus in bonuses]
        # Append row data
        data.append([eidolon_names] + bonuses)

        # For clean data, we only want the sums of the bonuses. Detect the numbers from the 3/4 star bonuses and 
        # sum them up, then put them back into their text form.
        cleaned = sum_sentences(bonuses[2], bonuses[3])
        data_cleaned.append([eidolon_names] + [cleaned])

    # Define CSV headers
    headers = ["Eidolon Names", "1 Star", "2 Star", "3 Star", "4 Star"]
    headers_clean = ["Eidolon Names", "Total Bonus"]
    # Save to CSV
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter="|")
        writer.writerow(headers)
        writer.writerows(data)
    
    with open(clean_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter="|")
        writer.writerow(headers_clean)
        writer.writerows(data_cleaned)

    print(f"Data successfully extracted to {output_file}")
    return True
