import os
import requests
import json
import logging
import uuid
from gtts import gTTS
from bs4 import BeautifulSoup
import urllib
from multiprocessing.pool import ThreadPool

dir_path = os.path.dirname(os.path.realpath(__file__))

def make_plain_text(s):
    return s.encode('utf-8').strip().decode("ascii","ignore")

def make_relative(filename):
    path = make_plain_text('/'.join((dir_path,filename)))
    return path

STATIC_DIR = make_relative("static")

# logging.basicConfig(make_relative("source.log"),
#                     filemode='w',
#                     level=logging.INFO)

with open(make_relative("config.json")) as f:
    api_key = json.load(f)["key"]


def fetch_articles(source, sort_by = "top"):
    """
    fetches the json from api
    """
    api_url = "https://newsapi.org/v1/articles?source={source}&sortBy={sort_by}&apiKey={api_key}"
    request_url = api_url.format(source=source,sort_by=sort_by,api_key=api_key)
    r = requests.get(request_url)
    if r.status_code != 200:
        print("The following error occurred: " + r.text)
        return
    data = r.text
    return json.loads(data)["articles"]

def article_body(html):
    soup = BeautifulSoup(html, "html.parser")
    story_body = soup.findAll("p" , {"class":"story-body-text story-content"})
    if story_body == None:
        return []
    paragraphs = [p.getText() for p in story_body]
    return paragraphs

# def log_articles(article):
#     """
#     writes the article information to a log file
#     """
#     title = article["title"]
#     author = article["author"]
#     url = article["url"]
#     published_date = article["publishedAt"]
#     content = article_body(requests.get(url).text)
#     message="{0}:{1}:{2}:{3}:{4}".format(title,
#                                         author,
#                                         url,
#                                         published_date,
#                                         content)
#     logging.info(message)

def orate_articles(article):
    title = article["title"]
    author = article["author"]
    url = article["url"]
    # date = article["publishedAt"]
    if not(os.path.exists(STATIC_DIR)):
        os.mkdir(STATIC_DIR)
    body = article_body(requests.get(url).text)
    if len(body) == 0:
        # logging.info("No story body for: " +  url)
        return {"title":title, "author":author, "url":url, "path":None}
    tts = gTTS(make_plain_text(''.join(body)), lang='en')
    path = make_plain_text("static" + '/' + title.split()[0] + '-' + str(uuid.uuid4()) + ".mp3")
    relative_path = make_relative(path)
    tts.save(relative_path)
    size = os.stat(relative_path).st_size
    return {"title":title, "author":author, "url":url, "path":path, "size":size}

def store_articles(articles):
    """
    multi thread all of the different urls
    """
    pool = ThreadPool(4) # TODO: the number of cores
    results = pool.map(orate_articles, articles)
    pool.close()
    pool.join()
    return results

def too_big(size):
    int_size = int(size)
    if int_size > 10000000:
        return True
    return False

def refresh(source):
    # find the old ones
    oldies = []
    if os.path.exists(STATIC_DIR):
        for f in os.listdir(STATIC_DIR):
            oldies.append(f)
    articles = fetch_articles(source)
    metadata = []
    for m in store_articles(articles):
        if m["path"] == None:
            continue
        if too_big(m["size"]): # check if the file is really big
            continue
        metadata.append(m)
    with open(make_relative('metadata.json'), 'w') as f:
        json.dump(metadata, f)
    # delete old ones
    for o in oldies:
        os.remove('/'.join((STATIC_DIR, o)))


if __name__ == "__main__":
    refresh("the-new-york-times")
