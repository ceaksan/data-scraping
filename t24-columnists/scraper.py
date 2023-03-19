import os
import requests
from bs4 import BeautifulSoup
import json
import re

# Read the data from the text file
with open("columnist-name.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Create the main directory
main_dir = "t24_columnists"
if not os.path.exists(main_dir):
    os.mkdir(main_dir)

# Loop through the data items
for item in data:
    # Extract the author name and identifier from the path
    path_parts = item["path"].split("/")
    author = path_parts[4]
    identifier = path_parts[-1].split(",")[1]

    # Create the subdirectory
    sub_dir = os.path.join(main_dir, author, identifier)
    os.makedirs(sub_dir, exist_ok=True)

    # Scrape the page and save the HTML file
    response = requests.get(item["path"])
    soup = BeautifulSoup(response.content, "html.parser")
    with open(os.path.join(sub_dir, "page.html"), "w", encoding="utf-8") as f:
        f.write(str(soup))

    # Create a clean text file and save it as Markdown
    with open(os.path.join(sub_dir, "page.md"), "w", encoding="utf-8") as f:
        # Get the title
        title = soup.find("h1").get_text().strip()

        # Get the description
        desc = soup.find("h2").get_text().strip()

        # Get the content
        content = soup.find("div", {"class": "_1NMxy"}).find_all(["p"])
        content_text = ""
        for elem in content:
            text = elem.get_text().strip()
            # Remove any newlines and multiple spaces
            text = re.sub("\s+", " ", text)
            content_text += text + "\n\n"

        # Write the Markdown file
        f.write("# " + title + "\n\n")
        f.write(desc + "\n\n")
        f.write(content_text)
