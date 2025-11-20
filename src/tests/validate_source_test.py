import unittest
from util import UserInputError
import util

class TestTodoValidation(unittest.TestCase):
    def setUp(self):
        pass

    def test_valid_length_does_not_raise_error(self):
        util.validate_key("valid")
        util.validate_key("a" * 100)

        util.validate_author("valid")
        util.validate_author("a" * 100)

        util.validate_title("valid")
        util.validate_title("a" * 100)

        util.validate_journal("valid")
        util.validate_journal("a" * 100)

        util.validate_publisher("valid")
        util.validate_publisher("a" * 100)

    def test_too_short_raises_error(self):
        with self.assertRaises(UserInputError):
            util.validate_key("abc")
        with self.assertRaises(UserInputError):
            util.validate_title("abc")
        with self.assertRaises(UserInputError):
            util.validate_journal("abc")
        with self.assertRaises(UserInputError):
            util.validate_publisher("abc")


    def test_too_long_raises_error(self):
        with self.assertRaises(UserInputError):
            util.validate_key("valid" * 21)
        with self.assertRaises(UserInputError):
            util.validate_author("valid" * 21)
        with self.assertRaises(UserInputError):
            util.validate_title("valid" * 21)
        with self.assertRaises(UserInputError):
            util.validate_journal("valid" * 21)
        with self.assertRaises(UserInputError):
            util.validate_publisher("valid" * 21)
    
    def test_valid_year(self):
        util.validate_year(2000)
        util.validate_year(2025)
    
    def test_invalid_year(self):
        with self.assertRaises(UserInputError):
            util.validate_year(-1)
        with self.assertRaises(UserInputError):
            util.validate_year("a")
    
    def test_valid_reference_type(self):
        util.validate_ref_type("article")
        util.validate_ref_type("book")
        util.validate_ref_type("inproceedings")
    
    def test_invalid_reference_type(self):
        with self.assertRaises(UserInputError):
            util.validate_ref_type("a")

    def test_validate_book(self):
        util.validate_book("valid", "book", "valid", "valid", "2025", "valid", "valid")