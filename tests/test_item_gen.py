"""Test the app's (shuffle) item generation module."""

import unittest
import item_gen

class TestitemGenerator(unittest.TestCase):
    """Test the functioning of the (shuffle) items generation module."""

    def test_a_certain_number_of_strings_with_a_certain_length_are_generated(self) -> None:
        """Confirm that a certain number of random strings with a certain length are generated."""

        strs = item_gen.random_strs(num=3, length=5)
        self.assertEqual(3, len(strs))
        self.assertEqual(5, len(strs[0]))
        self.assertEqual(5, len(strs[1]))
        self.assertEqual(5, len(strs[2]))
