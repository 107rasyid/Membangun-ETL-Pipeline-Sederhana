import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def scrape_page(page_url):
    """Scrape satu halaman dan kembalikan list of dict dengan fields dasar."""
    try:
        resp = requests.get(page_url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Request error di {page_url}: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    products = []
    for card in soup.select(".product-card"):
        try:
            title = card.select_one(".product-title").get_text(strip=True)
            price = card.select_one(".product-price").get_text(strip=True)
            rating = card.select_one(".product-rating").get_text(strip=True)
            colors = card.select_one(".product-colors").get_text(strip=True)
            size = card.select_one(".product-size").get_text(strip=True)
            gender = card.select_one(".product-gender").get_text(strip=True)
        except AttributeError as e:
            logger.warning(f"Missing field di {page_url}: {e}")
            continue

        products.append({
            "title": title,
            "price": price,
            "rating": rating,
            "colors": colors,
            "size": size,
            "gender": gender,
            # tambahkan timestamp ekstraksi
            "timestamp": datetime.utcnow().isoformat()
        })
    return products

def extract_all(pages=50):
    """Loop scraping dari halaman 1 sampai `pages`."""
    base = "https://fashion-studio.dicoding.dev/products?page={}"
    all_data = []
    for i in range(1, pages + 1):
        url = base.format(i)
        logger.info(f"Scraping halaman {i}: {url}")
        data = scrape_page(url)
        all_data.extend(data)
    return all_data