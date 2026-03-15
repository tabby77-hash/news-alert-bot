import requests
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PHONE = os.getenv("WHATSAPP_NUMBER")
TEXTMEBOT_KEY = os.getenv("TEXTMEBOT_KEY")

keywords = "Pakistan OR War OR Breaking"


def get_news():

    url = f"https://newsapi.org/v2/everything?q={keywords}&language=en&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"

    r = requests.get(url).json()

    headlines = []

    for article in r.get("articles", []):
        headlines.append(article["title"])

    return headlines


def gemini_filter(headlines):

    prompt = f"""
You are a global news intelligence filter.

From the following headlines detect ONLY major breaking news events
like war escalation, national emergency, military conflict or major disaster.

If nothing important return ONLY the word NONE.

Headlines:
{headlines}

If major news exists summarize it into ONE short sentence.
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    r = requests.post(url, json=payload)
    result = r.json()

    try:
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        return text.strip()
    except:
        return "NONE"


def is_duplicate(message):

    try:
        with open("last_news.txt", "r") as f:
            last = f.read().strip()
    except:
        last = ""

    if message == last:
        return True

    with open("last_news.txt", "w") as f:
        f.write(message)

    return False


def send_whatsapp(message):

    url = f"https://api.textmebot.com/send.php?recipient={PHONE}&text={message}&apikey={TEXTMEBOT_KEY}"

    requests.get(url)


def main():

    headlines = get_news()

    summary = gemini_filter(headlines)

    if summary == "NONE":
        print("No major news")
        return

    if is_duplicate(summary):
        print("Duplicate news")
        return

    send_whatsapp("Test message from my news bot!")

    print("Alert sent:", summary)


if _name_ == "_main_":
    main()
