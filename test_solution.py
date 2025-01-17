from solution import character_distribution

import pytest

# Test case 1: General input with mixed case and special characters
def test_general_case():
    assert character_distribution('Hello, World!') == {'H': 1, 'e': 1, 'l': 3, 'o': 2, 'W': 1, 'r': 1, 'd': 1}

# Test case 2: Empty string (Edge case)
def test_empty_string():
    assert character_distribution('') == {}

# Test case 3: String with no alphabetic characters (Edge case)
def test_no_alphabetic_characters():
    assert character_distribution('12345!@#$%') == {}

# Test case 4: String with all identical alphabetic characters
def test_identical_characters():
    assert character_distribution('aaaaaa') == {'a': 6}

# Test case 5: String with mixed letters and numbers
def test_mixed_letters_numbers():
    assert character_distribution('a1B2c3D4e5F6g7H8I9J0') == {'a': 1, 'B': 1, 'c': 1, 'D': 1, 'e': 1, 'F': 1, 'g': 1, 'H': 1, 'I': 1, 'J': 1}

# Test case 6: String with mixed case letters
def test_mixed_case():
    assert character_distribution('AaBbCcDdEe') == {'A': 1, 'a': 1, 'B': 1, 'b': 1, 'C': 1, 'c': 1, 'D': 1, 'd': 1, 'E': 1, 'e': 1}

# Test case 7: Large input with repetitive pattern (Performance case)
def test_large_input():
    large_input = 'abcde' * 1000
    expected_output = {'a': 1000, 'b': 1000, 'c': 1000, 'd': 1000, 'e': 1000}
    assert character_distribution(large_input) == expected_output

# Test case 8: String with mixed alphabetic and special characters
def test_mixed_alphabetic_special_characters():
    assert character_distribution('A!a@B#b$C%c^') == {'A': 1, 'a': 1, 'B': 1, 'b': 1, 'C': 1, 'c': 1}

# Test case 9: String with only special characters (Edge case)
def test_special_characters_only():
    assert character_distribution('!@#$%^&*()') == {}

# Test case 10: String with spaces and newlines
def test_string_with_spaces_and_newlines():
    assert character_distribution('A B\nC\tD') == {'A': 1, 'B': 1, 'C': 1, 'D': 1}
