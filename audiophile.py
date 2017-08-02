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

def make_relative(filename):
    path = '/'.join((dir_path,filename)).encode('utf-8').strip()
    return path

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
    r = requests.get(api_url.format(source=source,sort_by=sort_by,api_key=api_key))
    if r.status_code != 200:
        print("The following error occurred: " + r.text)
        return
    data = r.text
    return json.loads(data)["articles"]

def article_body(html):
    """
    soup = BeautifulSoup(html, "html.parser")
    story_body = soup.findAll("p") #, {"class":"story-body-text story-content"})
    if story_body == None:
        return []
    p_dict = {}
    for p in story_body:
        parent = p.parent
        if parent in p_dict:
            p_dict[parent].append(p)
        else:
            p_dict[parent] = [p]
    paragraphs = []
    p_len = -1
    for v in p_dict.values():
        if len(v) > p_len:
            paragraphs = v
            p_len = len(v)
    return [p.getText() for p in paragraphs]
    """
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

def orate_articles(article, directory="static"):
    title = article["title"]
    author = article["author"]
    url = article["url"]
    # date = article["publishedAt"]
    if not(os.path.exists(make_relative(directory))):
        os.mkdir(make_relative(directory))
    body = article_body(requests.get(url).text)
    if len(body) == 0:
        # logging.info("No story body for: " +  url)
        return {"title":title, "author":author, "url":url, "path":None}
    content = ''.join(body).encode('utf-8').strip()
    tts = gTTS(text=content.decode('utf-8'), lang='en')
    path = directory + '/' + title.split()[0] + '-' + str(uuid.uuid4()) + ".mp3"
    tts.save(make_relative(path))
    return {"title":title, "author":author, "url":url, "path":path}

def store_articles(articles):
    """
    multi thread all of the different urls
    """
    pool = ThreadPool(4) # TODO: the number of cores
    results = pool.map(orate_articles, articles)
    pool.close()
    pool.join()
    return results

def refresh(source):
    articles = fetch_articles(source)
    metadata = []
    for m in store_articles(articles):
        if m["path"] == None:
            continue
        metadata.append(m)
    with open(make_relative('metadata.json'), 'w') as f:
        json.dump(metadata, f)


if __name__ == "__main__":
    refresh("the-new-york-times")
