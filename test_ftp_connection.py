import unittest
import sys
import os
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from Helix import ClinicalDataProcessor
    HAS_HELIX = True
except ImportError:
    HAS_HELIX = False

class TestFTPConnection(unittest.TestCase):
    
    def setUp(self):
        self.test_host = "localhost"
        self.test_user = "testuser"
        self.test_pass = "testpass"
        self.mock_queue = Mock()
    
    @unittest.skipIf(not HAS_HELIX, "Helix module not available")
    @patch('ftplib.FTP')
    def test_successful_connection(self, mock_ftp_class):
        mock_ftp_instance = Mock()
        mock_ftp_class.return_value = mock_ftp_instance
        mock_ftp_instance.pwd.return_value = "/test/dir"
        
        processor = ClinicalDataProcessor(
            self.test_host,
            self.test_user,
            self.test_pass,
            "/test/dir"
        )
        
        result = processor.connect(self.mock_queue)
        
        self.assertTrue(result)
        self.assertTrue(processor.connected)
        mock_ftp_class.assert_called_once()
        mock_ftp_instance.connect.assert_called_once_with(self.test_host)
        mock_ftp_instance.login.assert_called_once_with(self.test_user, self.test_pass)
    
    @unittest.skipIf(not HAS_HELIX, "Helix module not available")
    @patch('ftplib.FTP')
    def test_failed_connection(self, mock_ftp_class):
        mock_ftp_instance = Mock()
        mock_ftp_class.return_value = mock_ftp_instance
        mock_ftp_instance.connect.side_effect = Exception("Connection refused")
        
        processor = ClinicalDataProcessor(
            self.test_host,
            self.test_user,
            self.test_pass
        )
        
        result = processor.connect(self.mock_queue)
        
        self.assertFalse(result)
        self.assertFalse(processor.connected)
    
    @unittest.skipIf(not HAS_HELIX, "Helix module not available")
    def test_disconnect(self):
        processor = ClinicalDataProcessor(
            self.test_host,
            self.test_user,
            self.test_pass
        )
        
        processor.ftp = Mock()
        processor.connected = True
        
        processor.disconnect()
        
        self.assertFalse(processor.connected)
        self.assertIsNone(processor.ftp)
    
    @unittest.skipIf(not HAS_HELIX, "Helix module not available")
    @patch('ftplib.FTP')
    def test_get_file_list(self, mock_ftp_class):
        mock_ftp_instance = Mock()
        mock_ftp_class.return_value = mock_ftp_instance
        mock_ftp_instance.nlst.return_value = [
            "CLINICALDATA20240101120000.CSV",
            "CLINICALDATA20240101120001.CSV",
            "README.txt",
            "config.ini"
        ]
        
        processor = ClinicalDataProcessor(
            self.test_host,
            self.test_user,
            self.test_pass
        )
        processor.ftp = mock_ftp_instance
        processor.connected = True
        
        files = processor.get_file_list(self.mock_queue)
        
        self.assertEqual(len(files), 2)
        self.assertIn("CLINICALDATA20240101120000.CSV", files)
        self.assertIn("CLINICALDATA20240101120001.CSV", files)
    
    @unittest.skipIf(not HAS_HELIX, "Helix module not available")
    def test_connection_status_without_ftp(self):
        processor = ClinicalDataProcessor(
            self.test_host,
            self.test_user,
            self.test_pass
        )
        
        files = processor.get_file_list(self.mock_queue)
        self.assertEqual(files, [])

class TestFTPIntegration(unittest.TestCase):
    
    @unittest.skipIf(not HAS_HELIX, "Helix module not available")
    def test_processor_initialization(self):
        processor = ClinicalDataProcessor(
            "ftp.example.com",
            "username",
            "password",
            "/remote/path"
        )
        
        self.assertEqual(processor.ftp_host, "ftp.example.com")
        self.assertEqual(processor.ftp_user, "username")
        self.assertEqual(processor.ftp_pass, "password")
        self.assertEqual(processor.remote_dir, "/remote/path")
        self.assertIsNone(processor.ftp)
        self.assertFalse(processor.connected)

if __name__ == "__main__":
    unittest.main()