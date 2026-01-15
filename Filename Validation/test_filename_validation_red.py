import pytest

def validate_filename(filename):
    return False

class TestFilenameValidation:
    def test_1_valid_filenames(self):
        assert validate_filename("document.pdf") == True
        assert validate_filename("image.png") == True
        assert validate_filename("data.csv") == True
    
    def test_2_invalid_characters(self):
        assert validate_filename("file<name.txt") == False
        assert validate_filename("doc:ument.pdf") == False
        assert validate_filename("data|file.csv") == False
    
    def test_3_length_limits(self):
        assert validate_filename("a.txt") == False
        assert validate_filename("ab.txt") == True
        assert validate_filename("abc.txt") == True
    
    def test_4_extensions(self):
        assert validate_filename("document") == False
        assert validate_filename("script.py") == True
        assert validate_filename("virus.exe") == False
    
    def test_5_empty_or_none(self):
        assert validate_filename("") == False
        assert validate_filename(None) == False
        assert validate_filename("   ") == False