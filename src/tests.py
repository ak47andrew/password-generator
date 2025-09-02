import pytest
import tempfile
import os
from converters import default, folder
from encoder import encode_old, encode_new, split_and_sum_with_interaction
from passwgen import main

def test_encode_old():
    """Test the old encoding function with simple input"""
    data = [0, 41, 50, 74, 41, 90, 69, 8, 68, 5, 58, 15, 73, 36, 79, 20, 63, 
            38, 4, 44, 89, 60, 2, 57, 12, 72, 7, 62, 24, 69, 40, 80, 24, 75, 
            41, 8, 48, 83, 53, 10, 70, 16, 51, 26, 72]
    output = "I~don't~know~what~to~put~into~this~test~text"
    result = encode_old(data, len(output))
    assert result == output

def test_encode_new():
    """Test the new encoding function with simple input"""
    data = [1, 2, 3, 4, 5]
    length = 5
    result = encode_new(data, length)
    assert result == "o|~T*"

def test_split_and_sum_with_interaction():
    """Test the split_and_sum_with_interaction function"""
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    length = 5
    result = split_and_sum_with_interaction(data, length)
    assert result == [6058483635957, 33652339540542, 109096670642871, 224162549156933, 224162559884775]

def test_default_converter():
    """Test the default converter with a temporary file"""
    # Create a temporary file with some content
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("test content")
        temp_path = f.name
    
    try:
        result = default(temp_path, silent=True)
        assert result == [116, 101, 115, 116, 32, 99, 111, 110, 116, 101, 110, 116]
    finally:
        # Clean up
        os.unlink(temp_path)

def test_folder_converter():
    """Test the folder converter with a temporary directory"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a few test files
        for i in range(3):
            with open(os.path.join(temp_dir, f"test{i}.txt"), "w") as f:
                f.write(f"test content {i}")
        
        result = folder(temp_dir, silent=True)
        assert result == [116, 101, 115, 116, 32, 99, 111, 110, 116, 101, 110, 116, 32, 48, 116, 
                          101, 115, 116, 32, 99, 111, 110, 116, 101, 110, 116, 32, 49, 116, 101, 
                          115, 116, 32, 99, 111, 110, 116, 101, 110, 116, 32, 50]

def test_default_converter_empty_file():
    """Test default converter with empty file"""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        temp_path = f.name
    try:
        result = default(temp_path, silent=True)
        assert result == []
    finally:
        os.unlink(temp_path)

def test_folder_converter_empty_folder():
    """Test folder converter with empty directory"""
    with tempfile.TemporaryDirectory() as temp_dir:
        result = folder(temp_dir, silent=True)
        assert result == []

def test_main_nonexistent_path():
    """Test main function with non-existent path"""
    with pytest.raises(SystemExit):
        main("nonexistent_path", None, 20, True)

def test_main_invalid_uri():
    """Test main function with invalid URI"""
    with pytest.raises(SystemExit):  # Technically it should be SystemExit with `exit(1)`, but it's TypeError becuase python and because pytest
        main(None, "invalid_uri", 20, True)

def test_integration_text_file():
    """Test complete pipeline with text file"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("test content")
        temp_path = f.name
    
    try:
        data = default(temp_path, True)
        old_result = encode_old(data, 10)
        new_result = encode_new(data, 10)
        assert len(old_result) == 10
        assert len(new_result) == 10
    finally:
        os.unlink(temp_path)

def test_special_characters_in_data():
    """Test encoders with special character values"""
    data = [0, 255, 1000, 0, 0]  # Edge case values
    result_old = encode_old(data, 10)
    result_new = encode_new(data, 10)
    # Verify results are valid strings
    assert isinstance(result_old, str)
    assert isinstance(result_new, str)

def test_large_file_handling():
    """Test performance with large files (might be marked as slow)"""
    large_data = list(range(10000))
    # Should complete in reasonable time
    result = encode_new(large_data, 20)
    assert len(result) == 20

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
