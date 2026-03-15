import requests
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PHONE = os.getenv("WHATSAPP_NUMBER")
CALLMEBOT_KEY = os.getenv("CALLMEBOT_KEY")

keywords = "Pakistan OR War OR Breaking"

def get_news():
    url = f"https://newsapi.org/v2/everything?q={keywords}&language=en&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"
    r = requests.get(url).json()
    headlines = [article["title"] for article in r["articles"]]
    return headlines


def gemini_filter(headlines):
    prompt = f"""
You are a news intelligence filter.
From the headlines below, detect if any represent MAJOR global or Pakistan related breaking news.
Ignore normal politics or minor stories.

Headlines:
{headlines}

If nothing major → return "NONE".
If major → summarize into ONE short alert sentence.
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    r = requests.post(url, json=payload)
    result = r.json()

    try:
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        return text.strip()
    except:
        return "NONE"


def check_duplicate(message):
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
    url = f"https://api.callmebot.com/whatsapp.php?phone={PHONE}&text={message}&apikey={CALLMEBOT_KEY}"
    requests.get(url)


def main():

    headlines = get_news()

    summary = gemini_filter(headlines)

    if summary == "NONE":
        print("No major news")
        return

    if check_duplicate(summary):
        print("Duplicate alert")
        return

    send_whatsapp(summary)

    print("Alert sent:", summary)


if _name_ == "_main_":
    main()
