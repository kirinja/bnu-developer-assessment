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
    
    # sort on items and based on publishing date, parse the str to a datetime so we can properly sort
    sorted_entries = sorted(entries.items(), key=lambda item: parse(item[1]['published']), reverse=True)

    # grab latest 10 entries from all sources
    return [(entry[0], entry[1]['id']) for entry in sorted_entries[:10]]


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def index():
    top_ten = feeds()
    return render_template("index.html", entries=top_ten)
