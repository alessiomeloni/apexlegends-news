# README

## Overview

This script is designed to scrape news articles from the "Apex Legends" section of the website [Everyeye](https://www.everyeye.it/notizie/apex-legends/) and store the article metadata in a TinyDB database. It performs the following main tasks:

1. Fetches the source content of the given URL.
2. Cleans the HTML content to extract clean text.
3. Scrapes article links from the base URL.
4. Scrapes detailed content from each article link.
5. Saves the article metadata to a TinyDB database if the article is not already present in the database.

## How to Use

1. Install the required libraries:
    ```bash
    pip install requests tinydb scrapy
    ```
2. Ensure you have the `news.json` file in the same directory as the script for TinyDB to store the data.
3. Run the script:
    ```bash
    python script_name.py
    ```

## Functions

- **get_source(url: str) -> Optional[requests.Response]**: Fetches the source content of the given URL using `requests` with a custom user-agent header.
- **clean_text(html_text: str) -> str**: Cleans HTML tags from the given text using Scrapy's `Selector`.
- **scrape_articles(base_url: str) -> List[str]**: Scrapes article links from the base URL.
- **scrape_content(link: str) -> Optional[Dict[str, str]>**: Scrapes the article metadata (title, content, media link) from the article URL.
- **save_to_db(db: TinyDB, article: Dict[str, str])**: Saves the article to the TinyDB database if it is not already present.
- **main()**: Main function to coordinate the scraping and saving process.

## Note

When I coded this script, I was just 14 years old and still learning the ropes of programming and web scraping. Originally, this was a module I created for a Telegram bot. As a result, the code might not be optimized or follow best practices. I've made some changes to the original code to make it work as a standalone script. Please bear with any inefficiencies or issues, as this was one of my earlier projects. I'm uploading it here on GitHub for nostalgic reasons and to preserve a piece of my programming journey.