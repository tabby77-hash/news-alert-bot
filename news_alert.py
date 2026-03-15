import requests
import feedparser
import os
import urllib.parse

RSS_URL = "https://www.dawn.com/feeds/home"

PHONE = os.getenv("WHATSAPP_NUMBER")
TEXTMEBOT_KEY = os.getenv("TEXTMEBOT_KEY")


def get_latest_news():

    print("Checking Dawn RSS...")

    feed = feedparser.parse(RSS_URL)

    if not feed.entries:
        print("No news found.")
        return None, None

    article = feed.entries[0]

    headline = article.title
    link = article.link

    return headline, link


def is_duplicate(message):

    try:
        with open("last_news.txt", "r") as f:
            last = f.read().strip()
    except:
        last = ""

    if message == last:
        print("Duplicate headline.")
        return True

    with open("last_news.txt", "w") as f:
        f.write(message)

    return False


def send_whatsapp(message):

    encoded = urllib.parse.quote(message)

    url = f"https://api.textmebot.com/send.php?recipient={PHONE}&text={encoded}&apikey={TEXTMEBOT_KEY}"

    r = requests.get(url)

    print("Status:", r.status_code)
    print("Response:", r.text)


def main():

    headline, link = get_latest_news()

    if not headline:
        return

    if is_duplicate(headline):
        return

    message = f"📰 Dawn Breaking News:\n{headline}\n\nRead more:\n{link}"

    send_whatsapp(message)

    print("Alert sent:", headline)


if __name__ == "__main__":
    main()
