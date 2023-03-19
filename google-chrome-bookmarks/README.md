# Chrome Bookmarks Organizer

This code is a Python script that allows you to scrape links from an HTML file and group them by domain. The script is designed to work with Google Chrome Bookmarks HTML files, but it can be used with any HTML file that contains links.

## How to Use

The scrape_html function is the main function of the script. It takes several arguments to customize the output, such as the input file path, output directory path, filename, extension, delimiter, and exclusion domains. You can also specify separate domains to save in separate files with their own filename.

To use the script, you need to import it into your Python code and call the scrape_html function with the appropriate arguments. The output will be saved to the specified output directory as a CSV or TXT file.

### Example Usage

Here is an example usage of the scrape_html function:

```python
scrape_html(
    input_path="/Users/user/Desktop/data-scraping/google-chome-bookmarks/bookmarks.html",
    output_dir="/Users/user/Desktop",
    filename="bookmark",
    extension="csv",
    strip_char="...",
    max_text_length=50,
    exclusion_domains=["facebook.com", "twitter.com"],
    separate_domains={
        "youtube.com": "youtube_links",
        "medium.com": "medium_links",
        "github.com": "github_links",
    }
)
```

This will scrape links from the `bookmarks.html` file and group them by domain. The output will be saved as a CSV file in the `output_dir` directory. The links will be stripped of the `strip_char` character, and the link text will be limited to `max_text_length` characters. Any links from the `exclusion_domains` list will be excluded from the output. Any domains specified in the `separate_domains` dictionary will be saved in separate CSV files with their own filename.