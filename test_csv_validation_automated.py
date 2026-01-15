import unittest
import tempfile
import csv
import os
import sys
from pathlib import Path
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from Helix import ClinicalDataValidator
    HAS_HELIX = True
except ImportError:
    HAS_HELIX = False

def generate_valid_csv(filename, num_records=5):
    rows = [
        ["PatientID", "TrialCode", "DrugCode", "Dosage_mg", 
         "StartDate", "EndDate", "Outcome", "SideEffects", "Analyst"]
    ]
    
    for i in range(1, num_records + 1):
        rows.append([
            f"P{i:03d}",
            f"TRIAL{i%3 + 1:03d}",
            f"DRUG{(i%5) + 1:03d}",
            str((i % 10 + 1) * 50),
            f"2024-{(i%12)+1:02d}-{(i%28)+1:02d}",
            f"2024-{((i%12)+2):02d}-{(i%28)+1:02d}",
            ["Improved", "No Change", "Worsened"][i % 3],
            ["None", "Mild", "Moderate", "Severe"][i % 4],
            f"ANALYST{(i%5)+1}"
        ])
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    
    return rows

def generate_invalid_csv(filename, error_type="dosage"):
    rows = [
        ["PatientID", "TrialCode", "DrugCode", "Dosage_mg", 
         "StartDate", "EndDate", "Outcome", "SideEffects", "Analyst"]
    ]
    
    if error_type == "dosage":
        rows.append(["P001", "T001", "D001", "-50", "2024-01-01", "2024-01-02", "Improved", "None", "A1"])
        rows.append(["P002", "T001", "D002", "not_a_number", "2024-01-01", "2024-01-02", "Improved", "None", "A1"])
    elif error_type == "date":
        rows.append(["P001", "T001", "D001", "100", "2024-01-02", "2024-01-01", "Improved", "None", "A1"])
    elif error_type == "outcome":
        rows.append(["P001", "T001", "D001", "100", "2024-01-01", "2024-01-02", "InvalidOutcome", "None", "A1"])
    elif error_type == "header":
        rows = [["Wrong", "Header", "Fields"], ["data", "here", "only"]]
    elif error_type == "missing_fields":
        rows.append(["P001", "T001", "", "100", "2024-01-01", "2024-01-02", "Improved", "None", "A1"])
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    
    return rows

class TestCSVValidation(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="csv_test_"))
        self.download_dir = self.temp_dir / "download"
        self.archive_dir = self.temp_dir / "archive"
        self.error_dir = self.temp_dir / "errors"
        
        for directory in [self.download_dir, self.archive_dir, self.error_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        if HAS_HELIX:
            self.validator = ClinicalDataValidator(
                str(self.download_dir),
                str(self.archive_dir),
                str(self.error_dir)
            )
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @unittest.skipIf(not HAS_HELIX, "Helix module not available")
    def test_valid_csv_validation(self):
        test_file = self.download_dir / "CLINICALDATA20240101120000.CSV"
        generate_valid_csv(test_file, num_records=3)
        
        is_valid, errors, valid_count = self.validator._validate_csv_content(
            test_file, status_queue=None
        )
        
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        self.assertEqual(valid_count, 3)
    
    @unittest.skipIf(not HAS_HELIX, "Helix module not available")
    def test_invalid_dosage_csv(self):
        test_file = self.download_dir / "CLINICALDATA20240101120001.CSV"
        generate_invalid_csv(test_file, error_type="dosage")
        
        is_valid, errors, valid_count = self.validator._validate_csv_content(
            test_file, status_queue=None
        )
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        self.assertIn("Dosage", str(errors))
    
    @unittest.skipIf(not HAS_HELIX, "Helix module not available")
    def test_invalid_date_csv(self):
        test_file = self.download_dir / "CLINICALDATA20240101120002.CSV"
        generate_invalid_csv(test_file, error_type="date")
        
        is_valid, errors, valid_count = self.validator._validate_csv_content(
            test_file, status_queue=None
        )
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
    
    @unittest.skipIf(not HAS_HELIX, "Helix module not available")
    def test_invalid_outcome_csv(self):
        test_file = self.download_dir / "CLINICALDATA20240101120003.CSV"
        generate_invalid_csv(test_file, error_type="outcome")
        
        is_valid, errors, valid_count = self.validator._validate_csv_content(
            test_file, status_queue=None
        )
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
    
    @unittest.skipIf(not HAS_HELIX, "Helix module not available")
    def test_empty_csv_file(self):
        test_file = self.download_dir / "CLINICALDATA20240101120004.CSV"
        with open(test_file, 'w', newline='', encoding='utf-8') as f:
            pass
        
        is_valid, errors, valid_count = self.validator._validate_csv_content(
            test_file, status_queue=None
        )
        
        self.assertFalse(is_valid)
        self.assertIn("empty", str(errors).lower())
    
    @unittest.skipIf(not HAS_HELIX, "Helix module not available")
    def test_duplicate_records(self):
        test_file = self.download_dir / "CLINICALDATA20240101120005.CSV"
        rows = [
            ["PatientID", "TrialCode", "DrugCode", "Dosage_mg", 
             "StartDate", "EndDate", "Outcome", "SideEffects", "Analyst"],
            ["P001", "T001", "D001", "100", "2024-01-01", "2024-01-02", "Improved", "None", "A1"],
            ["P001", "T001", "D001", "100", "2024-01-01", "2024-01-02", "Improved", "None", "A1"],
            ["P002", "T001", "D002", "200", "2024-01-01", "2024-01-02", "No Change", "Mild", "A2"]
        ]
        
        with open(test_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        
        is_valid, errors, valid_count = self.validator._validate_csv_content(
            test_file, status_queue=None
        )
        
        self.assertFalse(is_valid)
        has_duplicate_error = any("duplicate" in str(e).lower() for e in errors)
        self.assertTrue(has_duplicate_error)
        self.assertEqual(valid_count, 2)

def generate_sample_files():
    sample_dir = Path("sample_test_files")
    sample_dir.mkdir(exist_ok=True)
    
    valid_file = sample_dir / "valid_sample.csv"
    generate_valid_csv(valid_file, num_records=5)
    print(f"Generated: {valid_file}")
    
    for error_type in ["dosage", "date", "outcome"]:
        invalid_file = sample_dir / f"invalid_{error_type}_sample.csv"
        generate_invalid_csv(invalid_file, error_type)
        print(f"Generated: {invalid_file}")

if __name__ == "__main__":
    unittest.main()