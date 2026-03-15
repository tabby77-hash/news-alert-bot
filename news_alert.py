import requests
import os
import urllib.parse

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
PHONE = os.getenv("WHATSAPP_NUMBER")
TEXTMEBOT_KEY = os.getenv("TEXTMEBOT_KEY")


def get_news():

    url = f"https://newsapi.org/v2/top-headlines?sources=dawn-news&apiKey={NEWS_API_KEY}"

    print("Fetching Dawn headlines...")

    try:
        r = requests.get(url)
        data = r.json()

        articles = data.get("articles", [])

        if not articles:
            return None, None

        headline = articles[0]["title"]
        link = articles[0]["url"]

        return headline, link

    except Exception as e:
        print("News API error:", e)
        return None, None


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

    try:
        encoded_message = urllib.parse.quote(message)

        url = f"https://api.textmebot.com/send.php?recipient={PHONE}&text={encoded_message}&apikey={TEXTMEBOT_KEY}"

        r = requests.get(url)

        print("Status:", r.status_code)
        print("Response:", r.text)

    except Exception as e:
        print("WhatsApp error:", e)


def main():

    print("Bot started...")

    headline, link = get_news()

    if not headline:
        print("No headline found.")
        return

    if is_duplicate(headline):
        return

    message = f"📰 Dawn Headline:\n{headline}\n\nRead more: {link}"

    send_whatsapp(message)

    print("Headline sent:", headline)


if __name__ == "__main__":
    main()
