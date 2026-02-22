import unittest
from unittest.mock import patch
import sys
import io

from ragnarok.cli import main

class TestCLI(unittest.TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_help_output(self, mock_stdout):
        """Test that the CLI can be invoked and outputs help."""
        with patch.object(sys, 'argv', ['ragnarok', '--help']):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 0)
            self.assertIn("RAGnarok: The last file converter you'll ever need.", mock_stdout.getvalue())

if __name__ == "__main__":
    unittest.main()
