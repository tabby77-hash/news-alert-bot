import requests
import feedparser
import os
import urllib.parse

RSS_URL = "https://www.dawn.com/feeds/home"
LAST_FILE = "last_news.txt"

PHONE = os.getenv("WHATSAPP_NUMBER")
TEXTMEBOT_KEY = os.getenv("TEXTMEBOT_KEY")


def read_last_news():
    if os.path.exists(LAST_FILE):
        with open(LAST_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""


def save_last_news(headline):
    with open(LAST_FILE, "w", encoding="utf-8") as f:
        f.write(headline.strip())


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
    print("Fetching RSS feed...")
    feed = feedparser.parse(RSS_URL)
    if not feed.entries:
        print("No entries found in RSS.")
        return

    last_sent = read_last_news()
    print("Last sent headline:", last_sent)

    # Look for the first new headline
    for article in feed.entries:
        headline = article.title.strip()
        link = article.link.strip()
        if headline != last_sent:
            message = f"📰 Dawn Breaking News:\n{headline}\n\nRead more:\n{link}"
            send_whatsapp(message)
            save_last_news(headline)
            print("New headline sent:", headline)
            return  # stop after sending first new headline

    print("No new headlines to send.")


if __name__ == "__main__":
    main()
