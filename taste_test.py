import requests
from bs4 import BeautifulSoup

def load_cookies(filename="bggcookie.txt"):
    cookies = {}
    with open(filename, "r") as cookie_file:
        for line in cookie_file:
            parts = line.strip().split("\t")
            key, value = parts[5], parts[6]
            cookies[key] = value
    return cookies

def fetch_data_from_bgg(url):
    cookies = load_cookies()
    response = requests.get(url, cookies=cookies)

    if response.status_code == 200:
        content = response.content.decode("utf-8")
        return content
    else:
        print("Failed to fetch data.")
        return None

def extract_boardgames(content):
    """Extract board game names from HTML."""
    soup = BeautifulSoup(content, 'html.parser')
    games = soup.select(".collection_objectname a")
    for game in games:
        print(game.text)

if __name__ == "__main__":
    for i in range(1, 2): ## Good enough for now (Easy Change later)
        content = fetch_data_from_bgg(f"https://boardgamegeek.com/browse/boardgame/page/{i}")
        if content:
            extract_boardgames(content)
