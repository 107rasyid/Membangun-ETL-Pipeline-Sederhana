import re
import pandas as pd
import logging

logger = logging.getLogger(__name__)
EXCHANGE_RATE = 16_000

def clean_price(x: str) -> float | None:
    if not x or "Unavailable" in x:
        return None
    try:
        num = float(x.replace("$", "").replace(",", ""))
        return num * EXCHANGE_RATE
    except ValueError:
        return None

def clean_rating(x: str) -> float | None:
    """
    Cari angka pertama di string, misal 'Rating: ⭐ 4.8 / 5' → 4.8.
    Kembalikan None jika tidak ditemukan angka valid.
    """
    if not isinstance(x, str):
        return None
    match = re.search(r"(\d+(\.\d+)?)", x)
    return float(match.group(1)) if match else None

def clean_colors(x: str) -> int | None:
    if not isinstance(x, str):
        return None
    match = re.search(r"(\d+)", x)
    return int(match.group(1)) if match else None

def clean_size(x: str) -> str:
    if not isinstance(x, str):
        return ""
    return x.replace("Size:", "").strip()

def clean_gender(x: str) -> str:
    if not isinstance(x, str):
        return ""
    return x.replace("Gender:", "").strip()

def transform(data: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(data)

    # Clean and convert price
    df["price"] = df["price"].str.replace("[$,]", "", regex=True).astype(float) * 16000

    # Clean and convert rating
    df["rating"] = (
        df["rating"].str.extract(r"([\d.]+)").astype(float)
    )

    # Clean and convert colors
    df["colors"] = df["colors"].str.extract(r"(\d+)").astype(float)
    df["colors"] = df["colors"].astype(int)  # downcast dari float ke int

    # Drop baris yang tidak lengkap
    df = df.dropna(subset=["price", "rating", "colors", "size", "gender", "timestamp"])

    # Drop baris dengan title 'Unknown Product'
    df = df[df["title"] != "Unknown Product"]

    return df