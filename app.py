import json
import feedparser
from dateutil.parser import parse
from flask import Flask, render_template

app = Flask(__name__, template_folder="")


def feeds():
    with open("feeds.json") as obj:
        feeds = json.load(obj).get("feeds")
    
    # combine all feeds
    all_feeds = []
    for item in feeds:
        all_feeds.append(feedparser.parse(item))

    # create mapping between title and entry, this removes the duplicates
    entries = {}
    for item in all_feeds:
        for entry in item.entries:
            entries[entry.title] = entry
    
    sorted_entries = sort_dict_on_published((entries))

    # grab latest 10 entries from all sources
    return [(entry[0], entry[1]['id']) for entry in sorted_entries[:10]]


def sort_dict_on_published(items: dict, reverse:bool=True) -> dict:
    # sort on items and based on publishing date, parse the str to a datetime so we can properly sort
    sorted_items = sorted(items.items(), key=lambda item: parse(item[1]['published']), reverse=reverse)
    return sorted_items


async def parse_feed(feed_url: str) -> dict:
    feed = feedparser.parse(feed_url)
    entries = {}
    for item in feed.entries:
        entries[item.title] = item
    
    return entries


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def index():
    top_ten = feeds()
    return render_template("index.html", entries=top_ten)


@app.route("/async-route", methods=["GET"])
async def async_route():
    combined_entries = {}
    with open("feeds.json") as obj:
        temp = json.load(obj).get("feeds")
    
    for item in temp:
        combined_entries.update(await parse_feed(item))
    
    return render_template("index.html", entries=sort_dict_on_published(combined_entries)[:10])