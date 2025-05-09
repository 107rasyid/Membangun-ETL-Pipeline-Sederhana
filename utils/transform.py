import pandas as pd
import logging

logger = logging.getLogger(__name__)

EXCHANGE_RATE = 16_000  # asumsi USD -> IDR

def clean_price(x: str) -> float:
    """Ubah '$123.45' → float rupiah, atau None jika invalid."""
    if not x or "Unavailable" in x:
        return None
    try:
        # strip '$' dan koma ribuan
        num = float(x.replace("$", "").replace(",", ""))
        return num * EXCHANGE_RATE
    except ValueError:
        return None

def clean_rating(x: str) -> float:
    """Ubah '4.8 / 5' → 4.8, atau None jika invalid."""
    try:
        return float(x.split()[0])
    except Exception:
        return None

def clean_colors(x: str) -> int:
    """Ubah '3 Colors' → 3, atau None jika invalid."""
    try:
        return int(x.split()[0])
    except Exception:
        return None

def clean_size(x: str) -> str:
    """Hapus prefix 'Size: ' bila ada."""
    return x.replace("Size:", "").strip()

def clean_gender(x: str) -> str:
    """Hapus prefix 'Gender: ' bila ada."""
    return x.replace("Gender:", "").strip()

def transform(raw_data: list[dict]) -> pd.DataFrame:
    """Bersihkan list of dict dan kembalikan DataFrame siap load."""
    df = pd.DataFrame(raw_data)
    # Terapkan cleaning
    df["price"]   = df["price"].apply(clean_price)
    df["rating"]  = df["rating"].apply(clean_rating)
    df["colors"]  = df["colors"].apply(clean_colors)
    df["size"]    = df["size"].apply(clean_size)
    df["gender"]  = df["gender"].apply(clean_gender)

    # Buang invalid / null
    before = len(df)
    df = df.dropna(subset=["title", "price", "rating", "colors", "size", "gender", "timestamp"])
    logger.info(f"Dropped {before - len(df)} rows karena nilai null/invalid")

    # Hapus duplikat berdasarkan semua kolom kecuali timestamp
    df = df.drop_duplicates(subset=["title", "price", "rating", "colors", "size", "gender"])

    # Reset index
    df = df.reset_index(drop=True)
    return df
