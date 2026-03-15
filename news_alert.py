import requests
import feedparser
import os
import urllib.parse
import json
import subprocess

RSS_URL = "https://www.dawn.com/feeds/home"
LAST_FILE = "last_news.json"

PHONE = os.getenv("WHATSAPP_NUMBER")
TEXTMEBOT_KEY = os.getenv("TEXTMEBOT_KEY")
GH_TOKEN = os.getenv("GH_TOKEN")


def read_last_news():
    if os.path.exists(LAST_FILE):
        with open(LAST_FILE, "r", encoding="utf-8") as f:
            try:
                return set(json.load(f))
            except:
                return set()
    return set()


def save_last_news(headlines):
    with open(LAST_FILE, "w", encoding="utf-8") as f:
        json.dump(list(headlines), f)


def commit_last_news():
    subprocess.run(["git", "config", "--global", "user.name", "news-bot"])
    subprocess.run(["git", "config", "--global", "user.email", "bot@example.com"])
    subprocess.run(["git", "add", LAST_FILE])
    subprocess.run(["git", "commit", "-m", "Update last news"], check=False)
    # push using token
    repo_url = f"https://{GH_TOKEN}@github.com/{os.getenv('GITHUB_REPOSITORY')}.git"
    subprocess.run(["git", "push", repo_url, "HEAD:main"], check=False)


def send_whatsapp(message):
    encoded = urllib.parse.quote(message)
    url = f"https://api.textmebot.com/send.php?recipient={PHONE}&text={encoded}&apikey={TEXTMEBOT_KEY}"
    try:
        r = requests.get(url)
        print("WhatsApp Status:", r.status_code)
        print("WhatsApp Response:", r.text)
    except Exception as e:
        print("Error sending WhatsApp:", e)


def main():
    feed = feedparser.parse(RSS_URL)
    if not feed.entries:
        print("No entries found in RSS.")
        return

    last_sent = read_last_news()
    print("Previously sent headlines:", last_sent)

    new_sent = set()
    for article in feed.entries:
        headline = article.title.strip()
        link = article.link.strip()
        if headline not in last_sent:
            message = f"📰 Dawn Breaking News:\n{headline}\n\nRead more:\n{link}"
            send_whatsapp(message)
            new_sent.add(headline)
            print("Sent headline:", headline)
            break  # send only one new headline per run

    # update last_news.json
    all_sent = last_sent.union(new_sent)
    save_last_news(all_sent)
    if new_sent:
        commit_last_news()


if __name__ == "__main__":
    main()
