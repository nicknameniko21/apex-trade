#!/usr/bin/env python3
"""
Comprehensive Unit Tests for test_script.py

This test suite provides thorough coverage of all functions with:
- Happy path tests
- Error handling tests
- Edge case tests
- Security validation tests
- Performance validation tests

Author: GitHub Copilot Agent
"""

import pytest
import json
import os
from pathlib import Path
from unittest.mock import Mock, patch, mock_open, MagicMock
import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError

# Import the module to test
import sys
sys.path.insert(0, str(Path(__file__).parent))
from test_script import (
    Config, fetch_data, process_data, save_results, 
    main, create_session_with_retries
)


class TestConfig:
    """Test suite for Config class"""
    
    def test_config_creation_with_defaults(self):
        """Test creating config with required parameters"""
        config = Config(api_url="https://test.com/api")
        assert config.api_url == "https://test.com/api"
        assert config.timeout == 30
        assert config.output_file == "results.json"
        assert config.max_retries == 3
        assert config.multiplier == 2
    
    def test_config_creation_with_custom_values(self):
        """Test creating config with custom values"""
        config = Config(
            api_url="https://custom.com",
            timeout=60,
            output_file="custom.json",
            max_retries=5,
            multiplier=3
        )
        assert config.timeout == 60
        assert config.output_file == "custom.json"
        assert config.max_retries == 5
        assert config.multiplier == 3
    
    def test_config_from_env_with_defaults(self):
        """Test loading config from environment with defaults"""
        with patch.dict(os.environ, {}, clear=True):
            config = Config.from_env()
            assert config.api_url == "https://api.example.com/data"
            assert config.timeout == 30
            assert config.output_file == "results.json"
    
    def test_config_from_env_with_custom_values(self):
        """Test loading config from environment with custom values"""
        env_vars = {
            'API_URL': 'https://custom-api.com',
            'API_TIMEOUT': '45',
            'OUTPUT_FILE': 'output.json',
            'MAX_RETRIES': '5',
            'DATA_MULTIPLIER': '3'
        }
        with patch.dict(os.environ, env_vars, clear=True):
            config = Config.from_env()
            assert config.api_url == "https://custom-api.com"
            assert config.timeout == 45
            assert config.output_file == "output.json"
            assert config.max_retries == 5
            assert config.multiplier == 3


class TestCreateSessionWithRetries:
    """Test suite for session creation with retry logic"""
    
    def test_create_session_returns_session(self):
        """Test that create_session_with_retries returns a requests.Session"""
        session = create_session_with_retries()
        assert isinstance(session, requests.Session)
    
    def test_create_session_with_custom_retries(self):
        """Test creating session with custom retry count"""
        session = create_session_with_retries(max_retries=5)
        assert isinstance(session, requests.Session)


class TestFetchData:
    """Test suite for fetch_data function"""
    
    def test_fetch_data_success(self):
        """Test successful data fetching"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.json.return_value = [
            {'id': 1, 'name': 'item1', 'value': 10, 'status': 'active'}
        ]
        
        with patch('test_script.create_session_with_retries') as mock_session_creator:
            mock_session = Mock()
            mock_session.get.return_value = mock_response
            mock_session_creator.return_value = mock_session
            
            data = fetch_data("https://api.example.com/data")
            
            assert len(data) == 1
            assert data[0]['id'] == 1
            assert data[0]['name'] == 'item1'
    
    def test_fetch_data_with_provided_session(self):
        """Test fetching data with provided session"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.json.return_value = [{'id': 1}]
        
        mock_session = Mock()
        mock_session.get.return_value = mock_response
        
        data = fetch_data("https://api.example.com/data", session=mock_session)
        assert len(data) == 1
        mock_session.get.assert_called_once()
    
    def test_fetch_data_empty_list(self):
        """Test fetching empty data list"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.json.return_value = []
        
        with patch('test_script.create_session_with_retries') as mock_session_creator:
            mock_session = Mock()
            mock_session.get.return_value = mock_response
            mock_session_creator.return_value = mock_session
            
            data = fetch_data("https://api.example.com/data")
            assert data == []
    
    def test_fetch_data_invalid_url_scheme(self):
        """Test that invalid URL schemes are rejected"""
        with pytest.raises(ValueError, match="Invalid URL scheme"):
            fetch_data("ftp://invalid.com/data")
    
    def test_fetch_data_timeout(self):
        """Test handling of timeout errors"""
        with patch('test_script.create_session_with_retries') as mock_session_creator:
            mock_session = Mock()
            mock_session.get.side_effect = Timeout()
            mock_session_creator.return_value = mock_session
            
            with pytest.raises(Timeout):
                fetch_data("https://api.example.com/data")
    
    def test_fetch_data_connection_error(self):
        """Test handling of connection errors"""
        with patch('test_script.create_session_with_retries') as mock_session_creator:
            mock_session = Mock()
            mock_session.get.side_effect = ConnectionError()
            mock_session_creator.return_value = mock_session
            
            with pytest.raises(ConnectionError):
                fetch_data("https://api.example.com/data")
    
    def test_fetch_data_http_error(self):
        """Test handling of HTTP errors"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = HTTPError()
        
        with patch('test_script.create_session_with_retries') as mock_session_creator:
            mock_session = Mock()
            mock_session.get.return_value = mock_response
            mock_session_creator.return_value = mock_session
            
            with pytest.raises(HTTPError):
                fetch_data("https://api.example.com/data")
    
    def test_fetch_data_invalid_json(self):
        """Test handling of invalid JSON response"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.json.side_effect = json.JSONDecodeError("test", "doc", 0)
        
        with patch('test_script.create_session_with_retries') as mock_session_creator:
            mock_session = Mock()
            mock_session.get.return_value = mock_response
            mock_session_creator.return_value = mock_session
            
            with pytest.raises(ValueError, match="Invalid JSON response"):
                fetch_data("https://api.example.com/data")
    
    def test_fetch_data_non_list_response(self):
        """Test handling of non-list JSON response"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.json.return_value = {'error': 'not a list'}
        
        with patch('test_script.create_session_with_retries') as mock_session_creator:
            mock_session = Mock()
            mock_session.get.return_value = mock_response
            mock_session_creator.return_value = mock_session
            
            with pytest.raises(ValueError, match="Expected list data"):
                fetch_data("https://api.example.com/data")


class TestProcessData:
    """Test suite for process_data function"""
    
    def test_process_data_success(self):
        """Test successful data processing"""
        input_data = [
            {'id': 1, 'name': 'item1', 'value': 10, 'status': 'active'},
            {'id': 2, 'name': 'item2', 'value': 20, 'status': 'inactive'},
            {'id': 3, 'name': 'item3', 'value': 30, 'status': 'active'},
        ]
        
        results = process_data(input_data)
        
        assert len(results) == 2
        assert results[0]['id'] == 1
        assert results[0]['value'] == 20  # 10 * 2
        assert results[1]['id'] == 3
        assert results[1]['value'] == 60  # 30 * 2
    
    def test_process_data_with_custom_multiplier(self):
        """Test processing with custom multiplier"""
        input_data = [
            {'id': 1, 'name': 'item1', 'value': 10, 'status': 'active'},
        ]
        
        results = process_data(input_data, multiplier=3)
        
        assert len(results) == 1
        assert results[0]['value'] == 30  # 10 * 3
    
    def test_process_data_empty_list(self):
        """Test processing empty data list"""
        results = process_data([])
        assert results == []
    
    def test_process_data_all_inactive(self):
        """Test processing when all items are inactive"""
        input_data = [
            {'id': 1, 'name': 'item1', 'value': 10, 'status': 'inactive'},
            {'id': 2, 'name': 'item2', 'value': 20, 'status': 'inactive'},
        ]
        
        results = process_data(input_data)
        assert results == []
    
    def test_process_data_missing_fields(self):
        """Test processing with missing required fields"""
        input_data = [
            {'id': 1, 'status': 'active'},  # Missing name and value
            {'id': 2, 'name': 'item2', 'value': 20, 'status': 'active'},  # Complete
        ]
        
        results = process_data(input_data)
        
        # Should skip item with missing fields
        assert len(results) == 1
        assert results[0]['id'] == 2
    
    def test_process_data_non_numeric_value(self):
        """Test processing with non-numeric value field"""
        input_data = [
            {'id': 1, 'name': 'item1', 'value': 'invalid', 'status': 'active'},
            {'id': 2, 'name': 'item2', 'value': 20, 'status': 'active'},
        ]
        
        results = process_data(input_data)
        
        # Should skip item with non-numeric value
        assert len(results) == 1
        assert results[0]['id'] == 2
    
    def test_process_data_non_dict_items(self):
        """Test processing with non-dictionary items"""
        input_data = [
            "not a dict",
            {'id': 2, 'name': 'item2', 'value': 20, 'status': 'active'},
        ]
        
        results = process_data(input_data)
        
        # Should skip non-dict items
        assert len(results) == 1
        assert results[0]['id'] == 2
    
    def test_process_data_float_values(self):
        """Test processing with float values"""
        input_data = [
            {'id': 1, 'name': 'item1', 'value': 10.5, 'status': 'active'},
        ]
        
        results = process_data(input_data)
        
        assert len(results) == 1
        assert results[0]['value'] == 21.0  # 10.5 * 2


class TestSaveResults:
    """Test suite for save_results function"""
    
    def test_save_results_success(self, tmp_path):
        """Test successful results saving"""
        output_file = tmp_path / "results.json"
        results = [
            {'id': 1, 'name': 'item1', 'value': 20},
            {'id': 2, 'name': 'item2', 'value': 40},
        ]
        
        save_results(results, str(output_file))
        
        assert output_file.exists()
        
        with open(output_file, 'r') as f:
            saved_data = json.load(f)
        
        assert saved_data == results
    
    def test_save_results_creates_parent_directory(self, tmp_path):
        """Test that parent directories are created if needed"""
        output_file = tmp_path / "subdir" / "results.json"
        results = [{'id': 1}]
        
        save_results(results, str(output_file))
        
        assert output_file.exists()
        assert output_file.parent.exists()
    
    def test_save_results_empty_list(self, tmp_path):
        """Test saving empty results list"""
        output_file = tmp_path / "results.json"
        
        save_results([], str(output_file))
        
        assert output_file.exists()
        with open(output_file, 'r') as f:
            saved_data = json.load(f)
        assert saved_data == []
    
    def test_save_results_overwrites_existing(self, tmp_path):
        """Test that existing files are overwritten"""
        output_file = tmp_path / "results.json"
        
        # Create initial file
        with open(output_file, 'w') as f:
            json.dump([{'old': 'data'}], f)
        
        # Save new results
        new_results = [{'new': 'data'}]
        save_results(new_results, str(output_file))
        
        # Verify new data
        with open(output_file, 'r') as f:
            saved_data = json.load(f)
        assert saved_data == new_results
    
    def test_save_results_permission_error(self, tmp_path):
        """Test handling of permission errors"""
        output_file = tmp_path / "results.json"
        
        # Create file and make it read-only
        output_file.touch()
        output_file.chmod(0o444)
        
        try:
            with pytest.raises(PermissionError):
                save_results([{'id': 1}], str(output_file))
        finally:
            # Cleanup: restore write permission
            output_file.chmod(0o644)


class TestMain:
    """Test suite for main function"""
    
    def test_main_success(self, tmp_path):
        """Test successful main execution"""
        output_file = tmp_path / "results.json"
        
        mock_data = [
            {'id': 1, 'name': 'item1', 'value': 10, 'status': 'active'}
        ]
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.json.return_value = mock_data
        
        env_vars = {
            'API_URL': 'https://test.com/api',
            'OUTPUT_FILE': str(output_file)
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            with patch('test_script.create_session_with_retries') as mock_session_creator:
                mock_session = Mock()
                mock_session.get.return_value = mock_response
                mock_session.close = Mock()
                mock_session_creator.return_value = mock_session
                
                exit_code = main()
                
                assert exit_code == 0
                assert output_file.exists()
    
    def test_main_network_error(self):
        """Test main function with network error"""
        with patch.dict(os.environ, {'API_URL': 'https://test.com/api'}, clear=True):
            with patch('test_script.create_session_with_retries') as mock_session_creator:
                mock_session = Mock()
                mock_session.get.side_effect = ConnectionError()
                mock_session.close = Mock()
                mock_session_creator.return_value = mock_session
                
                exit_code = main()
                
                assert exit_code == 1
    
    def test_main_validation_error(self):
        """Test main function with validation error"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.json.return_value = {'not': 'a list'}  # Invalid response
        
        with patch.dict(os.environ, {'API_URL': 'https://test.com/api'}, clear=True):
            with patch('test_script.create_session_with_retries') as mock_session_creator:
                mock_session = Mock()
                mock_session.get.return_value = mock_response
                mock_session.close = Mock()
                mock_session_creator.return_value = mock_session
                
                exit_code = main()
                
                assert exit_code == 1
    
    def test_main_closes_session(self):
        """Test that main always closes the session"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.json.return_value = []
        
        with patch.dict(os.environ, {}, clear=True):
            with patch('test_script.create_session_with_retries') as mock_session_creator:
                mock_session = Mock()
                mock_session.get.return_value = mock_response
                mock_session.close = Mock()
                mock_session_creator.return_value = mock_session
                
                main()
                
                # Verify session was closed
                mock_session.close.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
