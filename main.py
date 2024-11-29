from get_archive import get_html, parse

# Define URLs
url = "https://www.aurakingdom-db.com/charts/eidolon-archive"

# Download HTML file
get_html(url, "eidolon_archive.html")
parse("eidolon_archive.html", "eidolon_archive.csv")