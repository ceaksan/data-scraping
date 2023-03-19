# Web Scraping T24 Pages
This project involves scraping T24 pages and saving the content in both HTML and Markdown formats. The project consists of three main parts:

A JavaScript code that extracts information from a T24 page and outputs the data in JSON format.
A Python script that reads the JSON data, scrapes each page, and saves the content in HTML and Markdown formats.

## JavaScript Code
The JavaScript code is used to extract information from a T24 page and output the data in JSON format. The code uses a recursive function to scroll down the page and find new elements. Once all the elements have been found, the code extracts the necessary information (title, path, description, and date) and outputs the data in JSON format.

### JSON Data
The JSON data contains an array of objects, with each object representing a T24 page. The objects contain the following keys:

title
: the title of the page.

path
: the URL of the page.

description
: a brief description of the page.

date
: the date the page was published.

### Python Script
The Python script reads the JSON data and scrapes each T24 page. The script uses the BeautifulSoup library to parse the HTML and extract the necessary information (title, description, and content). The content is then saved in both HTML and Markdown formats.

To run the project, follow these steps:

- Open the JavaScript code in a web browser console and copy the JSON output.
- Save the JSON output in a text file with the name of the columnist as a txt file.
- Run the Python script by typing python scraper.py in the command line.
- The output files will be saved in the t24_scrapped_pages directory.
