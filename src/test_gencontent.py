import unittest
from gencontent import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_simple(self):
        actual = extract_title("# Привет")
        self.assertEqual(actual, "Привет")

if __name__ == "__main__":
    unittest.main()