import pytest

class FileValidator:
    MIN_NAME_LEN = 2
    VALID_EXT = {'pdf', 'png', 'csv', 'py', 'txt'}
    BAD_CHARS = {'<', '>', ':', '"', '|', '?', '*', '\\', '/'}
    
    @classmethod
    def validate(cls, filename):
        if filename is None:
            return False
        
        f = str(filename).strip()
        if not f:
            return False
        
        if '.' not in f:
            return False
        
        parts = f.rsplit('.', 1)
        if len(parts) != 2:
            return False
        
        name, ext = parts
        
        if len(name) < cls.MIN_NAME_LEN:
            return False
        
        if ext.lower() not in cls.VALID_EXT:
            return False
        
        for char in cls.BAD_CHARS:
            if char in name:
                return False
        
        if len(f) > 255:
            return False
        
        return True

def validate_filename(filename):
    return FileValidator.validate(filename)

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