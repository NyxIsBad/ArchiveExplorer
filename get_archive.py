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

def parse(input_file, output_file):
    with open(input_file, mode="r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Find the table with id="archive"
    table = soup.find("table", id="archive")

    # Extract data from each row
    rows = table.find("tbody").find_all("tr")
    data = []

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

    # Define CSV headers
    headers = ["Eidolon Names", "1 Star", "2 Star", "3 Star", "4 Star"]

    # Save to CSV
    output_file = "eidolon_archive.csv"
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter="|")
        writer.writerow(headers)
        writer.writerows(data)

    print(f"Data successfully extracted to {output_file}")
    return True
