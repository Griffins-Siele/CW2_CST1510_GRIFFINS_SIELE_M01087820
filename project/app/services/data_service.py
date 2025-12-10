"""Data service module (Week 8).

This module handles data loading and processing for analytics.
References Week 8 data management patterns.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Dict, List


class DataService:
    """Service for managing analytical data.
    
    Handles loading, processing, and querying datasets.
    """
    
    def __init__(self):
        """Initialize the DataService."""
        self.data_dir = Path("project/DATA")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._cache = {}
    
    def load_csv(self, filename: str) -> Optional[pd.DataFrame]:
        """Load a CSV file into a DataFrame.
        
        Args:
            filename: Name of CSV file in DATA folder
            
        Returns:
            DataFrame if successful, None otherwise
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not a valid CSV
        """
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        try:
            df = pd.read_csv(filepath)
            self._cache[filename] = df
            return df
        except pd.errors.ParserError as e:
            raise ValueError(f"Invalid CSV format: {e}")
        except Exception as e:
            raise Exception(f"Error loading CSV: {e}")
    
    def get_cached_data(self, filename: str) -> Optional[pd.DataFrame]:
        """Get cached data if available.
        
        Args:
            filename: Name of the cached file
            
        Returns:
            Cached DataFrame or None
        """
        return self._cache.get(filename)
    
    def filter_data(self, df: pd.DataFrame, **filters) -> pd.DataFrame:
        """Filter DataFrame based on column criteria.
        
        Args:
            df: DataFrame to filter
            **filters: Column=value pairs to filter on
            
        Returns:
            Filtered DataFrame
            
        Raises:
            ValueError: If filter columns don't exist
        """
        if df is None or df.empty:
            raise ValueError("DataFrame is None or empty")
        
        result = df.copy()
        
        for column, value in filters.items():
            if column not in result.columns:
                raise ValueError(f"Column '{column}' not found in DataFrame")
            result = result[result[column] == value]
        
        return result
    
    def get_summary_stats(self, df: pd.DataFrame, numeric_cols: Optional[List[str]] = None) -> Dict:
        """Get summary statistics for numeric columns.
        
        Args:
            df: DataFrame to analyze
            numeric_cols: Specific columns to analyze (optional)
            
        Returns:
            Dictionary of statistics
            
        Raises:
            ValueError: If DataFrame is empty
        """
        if df is None or df.empty:
            raise ValueError("DataFrame is empty")
        
        if numeric_cols is None:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        stats = {}
        for col in numeric_cols:
            if col in df.columns:
                stats[col] = {
                    'mean': df[col].mean(),
                    'median': df[col].median(),
                    'std': df[col].std(),
                    'min': df[col].min(),
                    'max': df[col].max()
                }
        
        return stats


# Create singleton instance
_data_service = DataService()


def get_data_service() -> DataService:
    """Get the DataService instance.
    
    Returns:
        The DataService singleton
    """
    return _data_service
