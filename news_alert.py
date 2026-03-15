import requests
import feedparser
import os
import urllib.parse

RSS_URL = "https://www.dawn.com/feeds/home"
LAST_FILE = "last_news.txt"

PHONE = os.getenv("WHATSAPP_NUMBER")
TEXTMEBOT_KEY = os.getenv("TEXTMEBOT_KEY")


def get_latest_news():
    """Fetch the latest news headline from Dawn RSS feed."""
    print("Checking Dawn RSS...")

    feed = feedparser.parse(RSS_URL)

    if not feed.entries:
        print("No news found.")
        return None, None

    article = feed.entries[0]
    headline = article.title.strip()
    link = article.link.strip()

    return headline, link


def read_last_news():
    """Return the last saved headline, or empty string if none."""
    if os.path.exists(LAST_FILE):
        with open(LAST_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""


def save_last_news(headline):
    """Save the latest headline safely."""
    with open(LAST_FILE, "w", encoding="utf-8") as f:
        f.write(headline.strip())


def is_duplicate(headline):
    """Check if the headline is the same as last run."""
    last = read_last_news()
    if headline == last:
        print("Duplicate headline detected.")
        return True

    save_last_news(headline)
    return False


def send_whatsapp(message):
    """Send the message to WhatsApp using TextMeBot API."""
    encoded = urllib.parse.quote(message)
    url = f"https://api.textmebot.com/send.php?recipient={PHONE}&text={encoded}&apikey={TEXTMEBOT_KEY}"

    try:
        r = requests.get(url)
        print("Status:", r.status_code)
        print("Response:", r.text)
    except Exception as e:
        print("Error sending WhatsApp message:", e)


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
