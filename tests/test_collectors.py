import pytest
from unittest.mock import Mock, patch
from src.collectors.base_collector import BaseCollector

class TestCollector(BaseCollector):
    def collect(self, **kwargs):
        return []

def test_base_collector():
    collector = TestCollector("test")
    assert collector.source_name == "test"
    assert collector.session is not None

@patch('src.collectors.base_collector.requests.get')
def test_make_request(mock_get):
    mock_get.return_value = Mock()
    mock_get.return_value.json.return_value = {"test": "data"}
    mock_get.return_value.raise_for_status = Mock()
    
    collector = TestCollector("test")
    result = collector._make_request("http://test.com")
    
    assert result == {"test": "data"}
    mock_get.assert_called_once()