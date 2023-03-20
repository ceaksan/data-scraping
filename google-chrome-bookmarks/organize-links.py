import os
import csv
import re
from urllib.parse import urlparse
from collections import Counter
from pathlib import Path
from bs4 import BeautifulSoup


def group_domains(url):
    """Group domain names based on their hostname."""
    parsed = urlparse(url)
    domain = parsed.netloc
    if domain.startswith('www.'):
        domain = domain[4:]
    if '.' in domain:
        match = re.search(r'\.[^.]+$', domain)
        if match:
            tld = match.group(0)
            domain = domain[:match.start()]
            return domain + tld
    return domain


def scrape_html(input_path: str, output_dir: str, filename: str = "bookmark", extension: str = "txt",
                delimiter: str = "\t", strip_char: str = None, max_text_length: int = None, exclusion_domains: list = [],
                separate_domains: dict = {}):
    """
    Scrape links from an HTML file and group them by domain.

    Args:
        input_path (str): Path to the input HTML file.
        output_dir (str): Path to the output directory.
        filename (str): Base filename for the output files.
        extension (str): File extension for the output files. Can be "txt" or "csv".
        delimiter (str): Field delimiter for the output files.
        strip_char (str): Character to strip from link text. Default is None.
        max_text_length (int): Maximum length of link text. Default is None (no limit).
        exclusion_domains (list): List of domains to exclude from the output.
        separate_domains (dict): Dictionary of domains to save in separate files with their own filename.

    Returns:
        None
    """
    input_path = Path(input_path)
    output_dir = Path(output_dir)

    # Check if input file exists
    if not input_path.is_file():
        print(f"Error: {input_path} does not exist.")
        return

    # Check if the directory exists
    if not os.path.exists(output_dir):
        print(f"Error: {output_dir} does not exist.")
        os.makedirs(output_dir)

    # Parse HTML file
    with input_path.open("r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Find all A tags and extract href and text
    links = [(a.get_text(strip=strip_char), a.get("href")) for a in soup.find_all("a")]

    # Group links by domain and count the number of links in each group
    domain_counts = Counter([group_domains(href) for text, href in links if group_domains(href) not in exclusion_domains])


    # Save links to file
    if extension == "csv":
        output_path = output_dir / f"{filename}.csv"
        with output_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=delimiter)
            writer.writerow(["Group", "URL", "Text"])
            for text, href in links:
                domain = group_domains(href)
                if domain not in exclusion_domains and (domain not in separate_domains or separate_domains.get(domain) == filename):
                    writer.writerow([domain, href, text[:max_text_length] if max_text_length else text])
        print(f"Links saved to {output_path}")
    else:
        output_path = output_dir / f"{filename}.txt"
        with output_path.open("w", encoding="utf-8") as f:
            for text, href in links:
                domain = group_domains(href)
                if domain not in exclusion_domains and (domain not in separate_domains or separate_domains.get(domain) == filename):
                    f.write(delimiter.join([domain, href, text[:max_text_length] if max_text_length else text]) + "\n")
        print(f"Links saved to {output_path}")

    # Save separate domain files
    for domain, file in separate_domains.items():
        if domain in domain_counts:
            output_path = output_dir / f"{file}.csv"
            with output_path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=delimiter)
                writer.writerow(["Group", "URL", "Text"])
                for text, href in links:
                    if group_domains(href) == domain:
                        writer.writerow([domain, href, text[:max_text_length] if max_text_length else text])
            print(f"{domain} links saved to {output_path}")
            
    # Print summary of link groups
    group_summary = Counter(domain_counts).most_common()
    print("\nLink Group Summary:")
    for group, count in group_summary:
        print(f"{group}: {count}")
        

# Example usage
scrape_html(
    input_path="/Users/user/Desktop/data-scraping/google-chrome-bookmarks/bookmarks.html",
    output_dir="/Users/user/Desktop/bookmarks",
    filename="bookmark",
    extension="csv",
    strip_char="...",
    max_text_length=50,
    exclusion_domains=["facebook.com", "twitter.com"],
    separate_domains={
        "youtube.com": "youtube_links",
        "eksisozluk.com": "eksisozluk_links",
        "medium.com": "medium_links",
        "etsy.com": "etsy_links",
        "github.com": "github_links",
        "tr.pinterest.com": "pinterest_links",
        "imdb.com": "imdb_links",
    }
)