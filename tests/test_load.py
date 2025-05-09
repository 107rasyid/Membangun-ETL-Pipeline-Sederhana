import pandas as pd
import pytest
import os
from utils.load import load_to_csv

def test_load_to_csv_creates_file(tmp_path, caplog):
    df = pd.DataFrame({
        "a": [1, 2],
        "b": ["x", "y"]
    })
    out = tmp_path / "out.csv"
    caplog.set_level("INFO")
    load_to_csv(df, output_path=str(out))
    # File ada
    assert out.exists()
    # Konten CSV sesuai
    df2 = pd.read_csv(str(out))
    pd.testing.assert_frame_equal(df, df2)
    # Log info
    assert "Data berhasil disimpan ke" in caplog.text

def test_load_to_csv_error(tmp_path, monkeypatch):
    # Simulasi error to_csv
    df = pd.DataFrame({"a": [1]})
    monkeypatch.setattr(pd.DataFrame, "to_csv", lambda self, path, index: (_ for _ in ()).throw(Exception("fail")))
    with pytest.raises(Exception):
        load_to_csv(df, output_path=str(tmp_path / "x.csv"))
