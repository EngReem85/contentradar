import pytest
import pandas as pd
from src.processing.cleaner import DataCleaner

def test_clean_html():
    cleaner = DataCleaner()
    html = "<p>Test <b>content</b></p>"
    result = cleaner.clean_html(html)
    assert result == "Test content"

def test_normalize_genres():
    cleaner = DataCleaner()
    genres = ["Action", "Drama"]
    result = cleaner.normalize_genres(genres)
    assert result == ["action", "drama"]

def test_clean_dataframe():
    cleaner = DataCleaner()
    df = pd.DataFrame({
        'title': ['Movie (2024)'],
        'description': ['<p>Test</p>'],
        'genres': ['Action,Drama'],
        'popularity': ['10.5']
    })
    
    result = cleaner.clean_dataframe(df)
    
    assert result['title'][0] == 'Movie'
    assert result['description'][0] == 'Test'
    assert result['genres'][0] == ['action', 'drama']
    assert result['popularity'][0] == 10.5