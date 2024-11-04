import unittest
from config_language import ConfigLanguage

class TestConfigLanguage(unittest.TestCase):
    def setUp(self):
        self.config_lang = ConfigLanguage()

    def test_basic_conversion(self):
        json_data = {
            "settings": {
                "width": 800,
                "height": 600,
                "fullscreen": False
            }
        }
        expected_output = (
            "settings = {\n"
            "  width = 800\n"
            "  height = 600\n"
            "  fullscreen = False\n"
            "}\n"
        )
        output = self.config_lang.parse_json(json_data)
        self.assertEqual(output, expected_output)

    def test_variable_declaration(self):
        json_data = {
            "var1": 100,
            "var2": 200
        }
        expected_output = (
            "var var1 = 100\n"
            "var var2 = 200\n"
        )
        output = self.config_lang.parse_json(json_data)
        self.assertEqual(output, expected_output)

    def test_expression_evaluation(self):
        json_data = {
            "constant": "[^10 + 5]"
        }
        expected_output = "var constant = 15\n"
        output = self.config_lang.parse_json(json_data)
        self.assertEqual(output, expected_output)

    def test_invalid_variable_name(self):
        json_data = {
            "123invalid": 42
        }
        with self.assertRaises(ValueError) as context:
            self.config_lang.parse_json(json_data)
        self.assertIn("Invalid variable name", str(context.exception))

    def test_unsupported_value_type(self):
        json_data = {
            "unsupported": ["list", "of", "values"]
        }
        with self.assertRaises(ValueError) as context:
            self.config_lang.parse_json(json_data)
        self.assertIn("Unsupported value type", str(context.exception))

if __name__ == "__main__":
    unittest.main()
