import pandas as pd
import pytest
import numpy as np  # <-- Tambahkan ini

from utils.transform import (
    clean_price, clean_rating, clean_colors,
    clean_size, clean_gender, transform
)

def test_clean_price_valid_and_invalid():
    assert clean_price("$1,000.00") == 1_000 * 16_000
    assert clean_price("Unavailable") is None
    assert clean_price("abc") is None

def test_clean_rating_extracts_number():
    assert clean_rating("Rating: ⭐ 4.8 / 5") == pytest.approx(4.8)
    assert clean_rating("Rating: ⭐ Not Rated") is None
    assert clean_rating("Invalid") is None

def test_clean_colors_extracts_int():
    assert clean_colors("3 Colors") == 3
    assert clean_colors("No Colors") is None

def test_clean_size_and_gender_strip_prefix():
    assert clean_size("Size: L") == "L"
    assert clean_size("XL") == "XL"
    assert clean_gender("Gender: Male") == "Male"
    assert clean_gender("Female") == "Female"

def test_transform_drops_invalid_and_unknown():
    raw = [
        # valid
        {"title": "Good", "price": "$1.00", "rating": "Rating: ⭐ 5 / 5",
         "colors": "1 Colors", "size": "Size: S", "gender": "Gender: F",
         "timestamp": "2025-05-01T00:00:00"},
        # unknown product (should drop)
        {"title": "Unknown Product", "price": "$2.00", "rating": "Rating: ⭐ 4 / 5",
         "colors": "2 Colors", "size": "Size: M", "gender": "Gender: M",
         "timestamp": "2025-05-01T00:00:00"},
        # invalid rating (no number)
        {"title": "BadRating", "price": "$1.00", "rating": "Rating: ⭐ Not Rated",
         "colors": "1 Colors", "size": "Size: S", "gender": "Gender: F",
         "timestamp": "2025-05-01T00:00:00"},
        # missing price
        {"title": "NoPrice", "price": None, "rating": "Rating: ⭐ 3 / 5",
         "colors": "1 Colors", "size": "Size: S", "gender": "Gender: F",
         "timestamp": "2025-05-01T00:00:00"},
    ]
    df = transform(raw)
    # Hanya 1 baris valid tersisa: title "Good"
    assert len(df) == 1
    row = df.iloc[0]
    assert row["title"] == "Good"
    assert isinstance(row["price"], float)
    assert isinstance(row["rating"], float)
    # colors harus int atau np.integer
    assert isinstance(row["colors"], (int, np.integer))  # <-- Perbaikan di sini

def test_transform_preserves_timestamp_and_casts_types():
    raw = [{"title": "X", "price": "$1.00", "rating": "Rating: ⭐ 4.2 / 5",
            "colors": "2 Colors", "size": "Size: M", "gender": "Gender: Unisex",
            "timestamp": "2025-05-01T12:34:56"}]
    df = transform(raw)
    assert df.loc[0, "timestamp"] == "2025-05-01T12:34:56"
    assert df.loc[0, "colors"] == 2