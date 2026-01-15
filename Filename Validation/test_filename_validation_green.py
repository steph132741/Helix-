import pytest

def validate_filename(filename):
    if filename is None:
        return False
    
    filename = str(filename).strip()
    
    if not filename:
        return False
    
    if len(filename) < 3:
        return False
    
    if '.' not in filename:
        return False
    
    parts = filename.rsplit('.', 1)
    if len(parts) != 2:
        return False
    
    name, ext = parts
    
    if len(name) < 2:
        return False
    
    valid_ext = {'pdf', 'png', 'csv', 'py', 'txt'}
    if ext.lower() not in valid_ext:
        return False
    
    invalid_chars = {'<', '>', ':', '"', '|', '?', '*', '\\', '/'}
    for char in invalid_chars:
        if char in name:
            return False
    
    if len(filename) > 255:
        return False
    
    return True

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