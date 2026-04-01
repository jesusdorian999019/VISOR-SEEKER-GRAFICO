"""Log processor module for parsing and cleaning Seeker logs."""
import pandas as pd
import numpy as np
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COLUMNS = [
    'OS', 'Platform', 'CPU Cores', 'RAM', 'GPU Vendor', 'GPU', 'Resolution',
    'Browser', 'IP', 'Continent', 'Country', 'Region', 'City', 'ISP',
    'Organization', 'Latitude', 'Longitude', 'Accuracy', 'Altitude',
    'Direction', 'Speed'
]

class LogProcessor:
    """Class to parse and clean Seeker log files."""
    
    def __init__(self):
        self.raw_df: Optional[pd.DataFrame] = None
        self.cleaned_df: Optional[pd.DataFrame] = None
    
    def parse_file(self, file_path: str) -> pd.DataFrame:
        """Parse CSV-like log file into DataFrame."""
        try:
            # Read without headers, use our column names
            df = pd.read_csv(file_path, header=None, names=COLUMNS, on_bad_lines='warn')
            if len(df.columns) != len(COLUMNS):
                logger.warning(f"Expected {len(COLUMNS)} columns, got {len(df.columns)}")
            self.raw_df = df
            logger.info(f"Parsed {len(df)} rows from {file_path}")
            return df
        except Exception as e:
            logger.error(f"Error parsing file: {e}")
            raise
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean DataFrame: handle NA, split resolution, numeric conversions."""
        cleaned = df.copy()
        
        # Replace "Not Available" and similar to NaN
        na_values = ['Not Available', 'N/A', 'na', '']
        cleaned = cleaned.replace(na_values, np.nan)
        
        # Split Resolution into width and height
        if 'Resolution' in cleaned.columns:
            def split_res(res: str) -> tuple:
                if pd.isna(res):
                    return np.nan, np.nan
                try:
                    w, h = str(res).split('x')
                    return int(w), int(h)
                except:
                    return np.nan, np.nan
            
            res_split = cleaned['Resolution'].apply(split_res).apply(pd.Series)
            cleaned['width'] = res_split[0]
            cleaned['height'] = res_split[1]
            # Drop original Resolution column or keep? Keep for ref
            cleaned.drop('Resolution', axis=1, inplace=True, errors='ignore')
        
        # Numeric conversions
        numeric_cols = ['CPU Cores', 'RAM', 'Latitude', 'Longitude', 'Accuracy', 
                       'Altitude', 'Direction', 'Speed', 'width', 'height']
        for col in numeric_cols:
            if col in cleaned.columns:
                cleaned[col] = pd.to_numeric(cleaned[col], errors='coerce')
        
        self.cleaned_df = cleaned
        logger.info("Data cleaning completed")
        return cleaned
