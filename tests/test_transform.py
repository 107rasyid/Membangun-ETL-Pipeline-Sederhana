import pandas as pd
import pytest
from utils.transform import (
    clean_price, clean_rating, clean_colors,
    clean_size, clean_gender, transform
)

def test_clean_price_valid_and_invalid():
    assert clean_price("$1,000.00") == 1_000 * 16_000
    assert clean_price("Unavailable") is None
    assert clean_price("abc") is None

def test_clean_rating_valid_and_invalid():
    assert clean_rating("4.8 / 5") == 4.8
    assert clean_rating("Invalid") is None

def test_clean_colors_valid_and_invalid():
    assert clean_colors("3 Colors") == 3
    assert clean_colors("No Colors") is None

def test_clean_size_and_gender():
    assert clean_size("Size: L") == "L"
    assert clean_size("XL") == "XL"
    assert clean_gender("Gender: Male") == "Male"
    assert clean_gender("Female") == "Female"

def test_transform_dataframe_cleanup():
    raw = [
        {"title": "A", "price": "$1.00", "rating": "5 / 5", "colors": "1 Colors",
         "size": "Size: S", "gender": "Gender: F", "timestamp": "2025-05-01T00:00:00"},
        # Duplikat A
        {"title": "A", "price": "$1.00", "rating": "5 / 5", "colors": "1 Colors",
         "size": "Size: S", "gender": "Gender: F", "timestamp": "2025-05-01T00:00:00"},
        # Invalid price
        {"title": "B", "price": "Unavailable", "rating": "4 / 5", "colors": "2 Colors",
         "size": "Size: M", "gender": "Gender: M", "timestamp": "2025-05-01T00:00:00"},
        # Missing field → akan dropna
        {"title": None, "price": "$2.00", "rating": "4 / 5", "colors": "2 Colors",
         "size": "Size: M", "gender": "Gender: M", "timestamp": "2025-05-01T00:00:00"},
    ]
    df = transform(raw)
    # Hanya 1 baris valid unik (judul A)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    row = df.iloc[0]
    # Cek tipe data
    assert isinstance(row["price"], float)
    assert isinstance(row["rating"], float)
    assert isinstance(row["colors"], int)
    assert isinstance(row["size"], str)
    assert isinstance(row["gender"], str)

def test_transform_preserves_timestamp():
    raw = [{"title": "X", "price": "$1.00", "rating": "5 / 5",
            "colors": "1 Colors", "size": "Size: S", "gender": "Gender: F",
            "timestamp": "2025-05-01T12:34:56"}]
    df = transform(raw)
    assert df.loc[0, "timestamp"] == "2025-05-01T12:34:56"
