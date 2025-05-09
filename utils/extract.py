import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def scrape_page(page_url: str) -> list[dict]:
    """
    Scrape satu halaman dan kembalikan list of dict dengan fields:
    title, price, rating, colors, size, gender, timestamp.
    """
    try:
        resp = requests.get(page_url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        logger.error(f"Request error di {page_url}: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    cards = soup.select("div.collection-card")
    if not cards:
        logger.warning(f"Tidak menemukan produk di {page_url}")
    products = []

    for card in cards:
        try:
            title = card.select_one("h3.product-title").get_text(strip=True)

            # Price bisa elemen <span class="price"> atau <p class="price">
            price_tag = card.select_one(".price")
            price = price_tag.get_text(strip=True) if price_tag else None

            # Rating: e.g. "Rating: ⭐ 4.8 / 5" atau "Rating: ⭐ Not Rated"
            rating_p = card.select_one(".product-details p")
            rating = rating_p.get_text(strip=True) if rating_p else None

            # Colors, Size, Gender pada p-tags selanjutnya
            p_tags = card.select(".product-details p")
            colors = p_tags[1].get_text(strip=True) if len(p_tags) > 1 else None
            size   = p_tags[2].get_text(strip=True) if len(p_tags) > 2 else None
            gender = p_tags[3].get_text(strip=True) if len(p_tags) > 3 else None

        except Exception as e:
            logger.warning(f"Parsing error di {page_url}: {e}")
            continue

        products.append({
            "title":     title,
            "price":     price,
            "rating":    rating,
            "colors":    colors,
            "size":      size,
            "gender":    gender,
            "timestamp": datetime.utcnow().isoformat()
        })

    return products


def extract_all(pages: int = 50) -> list[dict]:
    """
    Loop scraping dari halaman 1 sampai `pages`.
    URL: 
      - Halaman 1 -> https://fashion-studio.dicoding.dev
      - Halaman 2 -> https://fashion-studio.dicoding.dev/page2
      - ...
    """
    base = "https://fashion-studio.dicoding.dev"
    all_data: list[dict] = []

    for i in range(1, pages + 1):
        if i == 1:
            url = base
        else:
            url = f"{base}/page{i}"
        logger.info(f"Scraping halaman {i}: {url}")
        page_data = scrape_page(url)
        all_data.extend(page_data)

    return all_data