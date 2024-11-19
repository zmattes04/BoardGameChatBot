import requests

url = "http://www.boardgamegeek.com/browse/boardgame"
response = requests.get(url)  # Gets the HTML page.

if response.status_code == 200:  # Check if the request was successful.
    content = response.text  # The returned HTML content.
    # Do something with content here.
    print(content)  # Example: Print the HTML content.
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")