import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

def load_to_csv(df, output_path="products.csv"):
    """Simpan DataFrame ke CSV."""
    try:
        df.to_csv(output_path, index=False)
        logger.info(f"Data berhasil disimpan ke {output_path}")
    except Exception as e:
        logger.error(f"Gagal menyimpan CSV: {e}")
        raise

# Contoh tambahan fungsi untuk Google Sheets atau PostgreSQL bisa ditambahkan di sini