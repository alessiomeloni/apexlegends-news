import json
import logging
import requests
from tinydb import TinyDB, Query
from scrapy.selector import Selector

################
FORMAT = "[%(asctime)s] - %(levelname)s : %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
# logging.info(text)
# logging.warning(text)
# logging.error(text)
# logging.critical(text)
################


def sourceScraper(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }
    while True:
        try:
            logging.info(f"Getting source from [{url[:50]}]")
            source = requests.get(url, headers=headers)
            return source
        except Exception as e:
            logging.warning(f"Error while getting source from [{url}]\n\t[{e}]")


def clean(text):
    import re

    clean = re.compile("<.*?>")
    cleaned = re.sub(clean, "", text)
    cleaned = cleaned.split(".")[0:3]
    return ".".join(cleaned)


def engine():
    db = TinyDB("news.json", encoding="utf-8")
    newsDB = Query()

    while True:
        spider = Selector(
            sourceScraper("https://www.everyeye.it/notizie/apex-legends/")
        )
        articlesLinks = spider.xpath(
            '//*[@id="bodybg"]/div/div/div[2]/div[1]/div/div[1]/ul//article/div/a/@href'
        ).getall()
        for link in articlesLinks:
            spider = Selector(sourceScraper(link))
            title = spider.xpath(
                '//*[@id="bodybg"]/main/div/div[1]/div[1]/h1/text()'
            ).get()
            try:
                db.search(newsDB.newsTitle == title)[0]["newsTitle"]
            except IndexError:
                news = clean(spider.xpath('//*[@id="inread"]').get())
                image = spider.xpath(
                    '//*[@id="bodybg"]/main/div/div[1]/div[2]/img/@data-src'
                ).get()
                db.insert({"newsTitle": title, "image": image})
                return (title, news, image)


# prendo link news
# entro nella news
# prendo titolo
# prendo immagine
# prendo articolo
# salvo sul db
# divulgo
# riparto da capo (1 request every 180s)
