import unittest
from chatbot import get_response, is_exit_command, calculate

class TestRuleBasedChatbot(unittest.TestCase):
    def test_greeting(self):
        self.assertIn("Hello", get_response("hi"))

    def test_case_and_whitespace(self):
        self.assertIn("Python", get_response("  WHAT IS PYTHON  "))

    def test_calculation(self):
        self.assertEqual(calculate("what is 25 + 37?"), "25 + 37 = 62")

    def test_division_by_zero(self):
        self.assertIn("zero", get_response("10 / 0").lower())

    def test_date(self):
        self.assertIn("Today's date is", get_response("what day is it today"))

    def test_fallback(self):
        self.assertIn("predefined response", get_response("tell me an unknown thing"))

    def test_exit(self):
        self.assertTrue(is_exit_command("bye"))
        self.assertFalse(is_exit_command("hello"))

if __name__ == "__main__":
    unittest.main()
