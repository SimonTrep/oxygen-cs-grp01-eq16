from io import StringIO
import sys

import os
import unittest
from dotenv import load_dotenv

from src.main import Main

load_dotenv()

TICKETS = int(os.getenv("TICKETS"))
T_MAX = int(os.getenv("T_MAX"))
T_MIN = int(os.getenv("T_MIN"))


class TestOxygenCs(unittest.TestCase):
    def setUp(self):
        self.main = Main()

    def test_init_main(self):
        self.assertEqual(self.main.TICKETS, TICKETS)
        self.assertEqual(self.main.T_MAX, T_MAX)
        self.assertEqual(self.main.T_MIN, T_MIN)

    def test_send_action_to_hvac(self):
        output = self.get_print(self.main.send_action_to_hvac, "TurnOnAc")
        self.assertEqual(output, "{'Response': 'Activating AC for 2 ticks'}")

    def test_take_action_at_min(self):
        output = self.get_print(self.main.take_action, T_MIN)
        self.assertEqual(output, "{'Response': 'Activating Heater for 2 ticks'}")

    def test_take_action_under_min(self):
        output = self.get_print(self.main.take_action, T_MIN - 1)
        self.assertEqual(output, "{'Response': 'Activating Heater for 2 ticks'}")

    def test_take_action_at_max(self):
        output = self.get_print(self.main.take_action, T_MAX)
        self.assertEqual(output, "{'Response': 'Activating AC for 2 ticks'}")

    def test_take_action_over_max(self):
        output = self.get_print(self.main.take_action, T_MAX + 1)
        self.assertEqual(output, "{'Response': 'Activating AC for 2 ticks'}")

    def test_take_action_normal_temperature_min(self):
        output = self.get_print(self.main.take_action, T_MIN + 1)
        self.assertEqual(output, "")

    def test_take_action_normal_temperature_max(self):
        output = self.get_print(self.main.take_action, T_MAX - 1)
        self.assertEqual(output, "")

    def test_on_sensor_data_received(self):
        data = [{"data": "23.0", "date": "2023-10-25T02:20:31.7862399+00:00"}]

        output = self.get_print(self.main.on_sensor_data_received, data)
        self.assertEqual(output, "2023-10-25T02:20:31.7862399+00:00 --> 23.0")

    def get_print(self, action, *arg):
        original_stdout = sys.stdout
        sys.stdout = StringIO()
        action(*arg)
        output = sys.stdout.getvalue().strip()
        sys.stdout = original_stdout
        return output


if __name__ == "__main__":
    unittest.main()
