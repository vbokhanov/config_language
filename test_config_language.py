import unittest
from config_language import ConfigLanguage

class TestConfigLanguage(unittest.TestCase):
    def setUp(self):
        self.config_lang = ConfigLanguage()

    def test_dicts(self):
        json_data = {
            "settings": {
                "width": 800,
                "height": 600,
                "fullscreen": False,
                "inner_setting": {
                    "timer": 100,
                    "brightness": {
                        "with_backlight": 1000,
                        "without_backlight": 450
                    }
                }
            }
        }
        expected_output = (
            "settings = {\n"
            "  var width = 800\n"
            "  var height = 600\n"
            "  var fullscreen = False\n"
            "  inner_setting = {\n"
            "    var timer = 100\n"
            "    brightness = {\n"
            "      var with_backlight = 1000\n"
            "      var without_backlight = 450\n"
            "    }\n"
            "  }\n"
            "}\n"
        )
        output = self.config_lang.parse_json(json_data)
        self.assertEqual(output, expected_output)

    def test_functions(self):
        json_data = {
            "var1": 2,
            "var2": 1,
            "var3": "[^max(max(var1, 5), var2)]",
            "var4": "[^sqrt(var1)]"
        }
        expected_output = (
            "var var1 = 2\n"
            "var var2 = 1\n"
            "var var3 = 5\n"
            "var var4 = 1.4142135623730951\n"
        )
        output = self.config_lang.parse_json(json_data)
        self.assertEqual(output, expected_output)

    def test_arithmetic_operations(self):
        json_data = {
            "a": "[^10 + 25 - 3 * 5]",
            "b": "[^a * 2 - 15]",
            "c": "[^a + b + 5 - 20 * 7]",
            "d": {
                "e": "[^a * b * c - 125]"
            }
        }
        expected_output = (
            "var a = 20\n"
            "var b = 25\n"
            "var c = -90\n"
            "d = {\n"
            "  var e = -45125\n"
            "}\n"
        )
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
