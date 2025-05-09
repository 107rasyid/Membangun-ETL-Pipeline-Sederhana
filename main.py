import logging
from utils.extract import extract_all
from utils.transform import transform
from utils.load import load_to_csv

logging.basicConfig(level=logging.INFO)

def main():
    # Extract
    raw = extract_all(pages=50)

    # Transform
    df_clean = transform(raw)

    # Load
    load_to_csv(df_clean, output_path="products.csv")

if __name__ == "__main__":
    main()
