import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup


def scrape_health_packages(url):
    """Scrape health package data from the given URL."""
    try:
        # Create a session with automatic retries
        session = requests.Session()
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        session.mount("https://", HTTPAdapter(max_retries=retries))

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
        }
        response = session.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        packages = []

        # Find all health package cards on the page
        cards = soup.select("a[href*='health-packages']")

        for card in cards:
            text = card.get_text(separator=" | ", strip=True)
            if "Include" in text and ("Parameters" in text or "Tests" in text):
                packages.append(text)

        if not packages:
            # Fallback: grab all meaningful text from the page
            page_text = soup.get_text(separator="\n", strip=True)
            for line in page_text.split("\n"):
                if any(kw in line for kw in ["Parameters", "Include", "Panel", "Checkup", "Profile"]):
                    if len(line.strip()) > 20:
                        packages.append(line.strip())

        if not packages:
            return "No health packages found on this page."

        scraped_text = "\n\n".join(packages)
        return scraped_text

    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {e}"