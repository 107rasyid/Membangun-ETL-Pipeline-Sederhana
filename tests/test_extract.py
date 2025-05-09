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
    # HTML dengan satu product-card lengkap
    html = """
    <div class="product-card">
      <span class="product-title">Test Shirt</span>
      <span class="product-price">$10.00</span>
      <span class="product-rating">4.5 / 5</span>
      <span class="product-colors">2 Colors</span>
      <span class="product-size">Size: M</span>
      <span class="product-gender">Gender: Unisex</span>
    </div>
    """
    monkeypatch.setattr("requests.get", lambda url, timeout: DummyResponse(html))
    data = extract.scrape_page("http://dummy.url")
    assert isinstance(data, list)
    assert len(data) == 1
    item = data[0]
    # Cek semua field ada
    for field in ("title", "price", "rating", "colors", "size", "gender", "timestamp"):
        assert field in item
    assert item["title"] == "Test Shirt"
    assert item["price"] == "$10.00"
    assert item["rating"] == "4.5 / 5"
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
    # Monkey-patch scrape_page untuk tiap halaman
    calls = []
    def fake_scrape(url):
        calls.append(url)
        return [{"title": url}]
    monkeypatch.setattr("utils.extract", "scrape_page", fake_scrape)
    all_data = extract.extract_all(pages=3)
    assert len(all_data) == 3
    # URL tiap halaman
    assert calls == [
        "https://fashion-studio.dicoding.dev/products?page=1",
        "https://fashion-studio.dicoding.dev/products?page=2",
        "https://fashion-studio.dicoding.dev/products?page=3",
    ]
