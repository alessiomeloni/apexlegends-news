import requests
from tinydb import Query, TinyDB
from typing import Optional, Dict, List
from scrapy.selector import Selector


def get_source(url: str) -> Optional[requests.Response]:
    """
    Fetches the source content of the given URL.

    :param url: URL of the webpage to scrape
    :return: Response object if successful, None otherwise
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/75.0.3770.100 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response
    except requests.RequestException:
        return None


def clean_text(html_text: str) -> str:
    """
    Cleans HTML tags from the given text.

    :param html_text: HTML content to clean
    :return: Cleaned text
    """
    selector = Selector(text=html_text)
    return selector.xpath("string()").get()


def scrape_articles(base_url: str) -> List[str]:
    """
    Scrapes article links from the base URL.

    :param base_url: URL of the webpage to scrape
    :return: List of article links
    """
    source = get_source(base_url)
    if source:
        spider = Selector(text=source.text)
        links = spider.xpath("//article[@class='fvideogioco']/a/@href").getall()
        return links
    return []


def scrape_content(link: str) -> Optional[Dict[str, str]]:
    """
    Scrapes the article meta data.

    :param link: URL of the article to scrape
    :return: Dictionary containing article data
    """
    source = get_source(link)
    if source:
        spider = Selector(text=source.text)
        title = spider.xpath("//h1/text()").get()
        if title:
            news_html = spider.xpath('//*[@id="inread"]').get()
            news = clean_text(news_html) if news_html else ""
            media = (
                spider.xpath('//*[@id="heroBase64"]/@href').get()
                or spider.xpath('//*[@id="player_eye_3"]/iframe/@src').get()
            )
            print(title)
            return {"link": link, "title": title, "news": news, "media": media}
    return None


def save_to_db(db: TinyDB, article: Dict[str, str]):
    """
    Saves the article to the database if it's not already present.

    :param db: TinyDB database instance
    :param article: Dictionary containing article data
    """
    news_query = Query()
    if not db.search(news_query.link == article["link"]):
        db.insert(article)


def main():
    with TinyDB("news.json", encoding="utf-8") as db:
        base_url = "https://www.everyeye.it/notizie/apex-legends/"

        articles_links = scrape_articles(base_url)
        db_links_set = {article["link"] for article in db.all()}
        new_article_links = set(articles_links) - db_links_set

        print(f"Found {len(new_article_links)} new articles.")

        for link in new_article_links:
            article = scrape_content(link)
            if article:
                save_to_db(db, article)
                print(f"Saved article: {article['link']}")


if __name__ == "__main__":
    main()
