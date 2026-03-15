import requests
import os
import urllib.parse

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PHONE = os.getenv("WHATSAPP_NUMBER")
TEXTMEBOT_KEY = os.getenv("TEXTMEBOT_KEY")

keywords = "Pakistan OR War OR Breaking"


def get_news():

    url = f"https://newsapi.org/v2/everything?q={keywords}&language=en&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"

    print("Fetching news...")

    try:
        r = requests.get(url)
        data = r.json()

        headlines = []

        for article in data.get("articles", []):
            headlines.append(article["title"])

        print("Headlines:", headlines)

        return headlines

    except Exception as e:
        print("News API error:", e)
        return []


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

    print("Sending headlines to Gemini...")

    try:
        r = requests.post(url, json=payload)
        result = r.json()

        text = result["candidates"][0]["content"]["parts"][0]["text"]

        summary = text.strip()

        print("Gemini result:", summary)

        return summary

    except Exception as e:
        print("Gemini API error:", e)
        return "NONE"


def is_duplicate(message):

    try:
        with open("last_news.txt", "r") as f:
            last = f.read().strip()
    except:
        last = ""

    if message == last:
        print("Duplicate alert detected.")
        return True

    with open("last_news.txt", "w") as f:
        f.write(message)

    return False


def send_whatsapp(message):

    try:
        encoded_message = urllib.parse.quote(message)

        url = f"https://api.textmebot.com/send.php?recipient={PHONE}&text={encoded_message}&apikey={TEXTMEBOT_KEY}"

        print("Sending WhatsApp message...")

        r = requests.get(url)

        print("Status Code:", r.status_code)
        print("Response:", r.text)

    except Exception as e:
        print("WhatsApp sending error:", e)


def main():

    print("Bot started...")

    headlines = get_news()

    if not headlines:
        print("No headlines retrieved.")
        return

    summary = "🚨 Test alert from news bot"

    if summary == "NONE":
        print("No major news detected.")
        return

    if is_duplicate(summary):
        return

    send_whatsapp(summary)

    print("Alert sent successfully.")


if __name__ == "__main__":
    main()
