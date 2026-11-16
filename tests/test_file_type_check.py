#!/usr/bin/env python3

import unittest
import os
import sys

# Add the current directory to Python path to import client modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from client import read_file


class TestFileTypeCheck(unittest.TestCase):
    def test_reject_binary_file(self):
        """Test that binary files are rejected."""
        binary_file = "chunks/chunk_0_0.bin.v1"
        with self.assertRaises(ValueError):
            read_file(binary_file)

    def test_accept_text_file(self):
        """Test that text files are accepted."""
        text_file = "protocole.md"
        try:
            content = read_file(text_file)
            # Make sure we got some content
            self.assertIsInstance(content, str)
            self.assertGreater(len(content), 0)
        except Exception as e:
            self.fail(f"Text file reading failed: {e}")


if __name__ == '__main__':
    unittest.main()