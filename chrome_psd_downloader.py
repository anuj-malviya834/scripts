import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def fetch_drive_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "drive.google.com" in href:
            links.append(href)
    return links


def download_with_selenium(links, download_path="C:\\Users\\HP\\Downloads\\PSD_Files"):
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_path,  # all PSD in one folder
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    for i, link in enumerate(links, start=1):
        print(f"[{i}] Opening {link}")
        driver.get(link)
        time.sleep(5)

        try:
            # Check and click "Download anyway" button if present
            btn = driver.find_element(
                By.XPATH, "//button[contains(text(),'Download anyway')]"
            )
            btn.click()
            print(f"[{i}] Clicked 'Download Anyway'")
        except:
            print(f"[{i}] No warning, downloading directly")

        # Wait for download (Drive ke large files ko thoda time lagta hai)
        time.sleep(15)

    driver.quit()
    print("✅ All downloads attempted. Check your folder:", download_path)


if __name__ == "__main__":
    page_url = "https://www.studiopk.in/haldi-ceremony-album-design-psd-2/"
    drive_links = fetch_drive_links(page_url)
    print(f"Found {len(drive_links)} Google Drive links.")

    download_with_selenium(drive_links)
