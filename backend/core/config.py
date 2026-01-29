from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Data directories
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
