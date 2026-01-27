import unittest
import sys
import os
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from Helix import ClinicalDataValidator
    HAS_HELIX = True
except ImportError:
    HAS_HELIX = False

class TestUUIDAPI(unittest.TestCase):
    
    @unittest.skipIf(not HAS_HELIX, "Helix module not available")
    @patch('requests.get')
    def test_uuid_from_external_api_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = ["123e4567-e89b-12d3-a456-426614174000"]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        uuid = ClinicalDataValidator.generate_uuid_from_api()
        
        mock_get.assert_called_once_with(
            "https://www.uuidtools.com/api/generate/v4",
            timeout=5
        )
        
        self.assertIsInstance(uuid, str)
        self.assertTrue(len(uuid) > 0)
    
    @unittest.skipIf(not HAS_HELIX, "Helix module not available")
    @patch('requests.get')
    def test_uuid_api_timeout_fallback(self, mock_get):
        mock_get.side_effect = Exception("Timeout occurred")
        
        uuid = ClinicalDataValidator.generate_uuid_from_api()
        
        self.assertIsInstance(uuid, str)
        self.assertTrue(len(uuid) > 0)
        mock_get.assert_called_once()
    
    @unittest.skipIf(not HAS_HELIX, "Helix module not available")
    @patch('requests.get')
    def test_uuid_api_connection_error_fallback(self, mock_get):
        mock_get.side_effect = Exception("Connection error")
        
        uuid = ClinicalDataValidator.generate_uuid_from_api()
        
        self.assertIsInstance(uuid, str)
        self.assertTrue(len(uuid) > 0)
    
    @unittest.skipIf(not HAS_HELIX, "Helix module not available")
    @patch('requests.get')
    def test_uuid_api_invalid_response_fallback(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = Exception("Server error")
        mock_get.return_value = mock_response
        
        uuid = ClinicalDataValidator.generate_uuid_from_api()
        
        self.assertIsInstance(uuid, str)
        self.assertTrue(len(uuid) > 0)
    
    @unittest.skipIf(not HAS_HELIX, "Helix module not available")
    @patch('requests.get')
    def test_uuid_api_empty_response_fallback(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        uuid = ClinicalDataValidator.generate_uuid_from_api()
        
        self.assertIsInstance(uuid, str)
        self.assertTrue(len(uuid) > 0)
    
    @unittest.skipIf(not HAS_HELIX, "Helix module not available")
    @patch('requests.get')
    @patch('uuid.uuid4')
    def test_local_uuid_generation(self, mock_uuid4, mock_get):
        mock_uuid_instance = Mock()
        mock_uuid_instance.__str__ = Mock(return_value="98765432-1234-5678-9123-456789012345")
        mock_uuid4.return_value = mock_uuid_instance
        
        mock_get.side_effect = Exception("Network error")
        
        uuid = ClinicalDataValidator.generate_uuid_from_api()
        
        self.assertEqual(uuid, "98765432-1234-5678-9123-456789012345")

class TestUUIDIntegration(unittest.TestCase):
    
    @unittest.skipIf(not HAS_HELIX, "Helix module not available")
    def test_uuid_format_validity(self):
        uuid = ClinicalDataValidator.generate_uuid_from_api()
        
        self.assertIsInstance(uuid, str)
        self.assertTrue(36 >= len(uuid) >= 32)
        
        import re
        uuid_clean = uuid.replace('-', '')
        self.assertTrue(re.match(r'^[a-fA-F0-9]{32}$', uuid_clean))
    
    @unittest.skipIf(not HAS_HELIX, "Helix module not available")
    def test_uuid_uniqueness(self):
        uuids = []
        for _ in range(10):
            # Mock to ensure fallback to test uniqueness
            with patch('requests.get', side_effect=Exception("Test")):
                uuid = ClinicalDataValidator.generate_uuid_from_api()
                uuids.append(uuid)
        
        self.assertEqual(len(uuids), len(set(uuids)))
        
        for uuid in uuids:
            self.assertTrue(len(uuid) > 0)

if __name__ == "__main__":
    unittest.main()