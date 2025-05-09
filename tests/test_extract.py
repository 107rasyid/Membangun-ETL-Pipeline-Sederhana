import pytest
from utils import extract
from datetime import datetime

class DummyResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise Exception(f"HTTP {self.status_code}")

def test_scrape_page_success(monkeypatch):
    # HTML sesuai struktur collection-card
    html = """
    <div class="collection-card">
      <h3 class="product-title">Test Shirt</h3>
      <div class="price-container"><span class="price">$10.00</span></div>
      <div class="product-details">
        <p>Rating: ⭐ 4.5 / 5</p>
        <p>2 Colors</p>
        <p>Size: M</p>
        <p>Gender: Unisex</p>
      </div>
    </div>
    """
    monkeypatch.setattr("requests.get", lambda url, timeout: DummyResponse(html))
    data = extract.scrape_page("http://dummy.url")
    assert isinstance(data, list)
    assert len(data) == 1
    item = data[0]
    # Cek semua field ada dan ter-capture sesuai selector
    assert item["title"] == "Test Shirt"
    assert item["price"] == "$10.00"
    assert item["rating"].startswith("Rating:")
    assert item["colors"] == "2 Colors"
    assert item["size"] == "Size: M"
    assert item["gender"] == "Gender: Unisex"
    # Timestamp harus ISO format
    datetime.fromisoformat(item["timestamp"])

def test_scrape_page_http_error(monkeypatch):
    # Simulasi HTTP 500
    monkeypatch.setattr("requests.get", lambda url, timeout: DummyResponse("", status_code=500))
    data = extract.scrape_page("http://dummy.url")
    assert data == []  # error handling mengembalikan list kosong

def test_extract_all_aggregates(monkeypatch):
    calls = []
    def fake_scrape(url):
        calls.append(url)
        return [{"title": url}]
    # Patch langsung pada modul extract
    monkeypatch.setattr(extract, "scrape_page", fake_scrape)
    all_data = extract.extract_all(pages=3)
    assert len(all_data) == 3
    assert calls == [
        "https://fashion-studio.dicoding.dev",
        "https://fashion-studio.dicoding.dev/page2",
        "https://fashion-studio.dicoding.dev/page3",
    ]