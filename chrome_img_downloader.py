import os
import requests
from bs4 import BeautifulSoup

url = "https://www.freepsdking.com/haldi-ceremony-album-design-psd-free-download/"
folder = "downloads"
os.makedirs(folder, exist_ok=True)

# Fetch page
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find all links with .zip or .rar (most PSDs come in these)
links = [
    a["href"]
    for a in soup.find_all("a", href=True)
    if a["href"].endswith((".zip", ".rar"))
]

for link in links:
    file_name = os.path.join(folder, link.split("/")[-1])
    print(f"Downloading {file_name}...")
    r = requests.get(link, stream=True)
    with open(file_name, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

print("All downloads completed!")
