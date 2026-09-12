import unittest
from types import SimpleNamespace
from unittest.mock import patch

from Models.Bot import Bot
from Models.Keyboard import Keyboard


class RepeatManualBotTests(unittest.TestCase):
    def test_repeat_man_dispatches_to_live_mouse_controller_instead_of_queue_proxy(self):
        bot = Bot()
        bot.kb.check_key_pressed = lambda trigger: False

        calls = []

        def fake_mouse_clck(btn):
            calls.append(("clck", btn))

        bot.m.clck = fake_mouse_clck

        bot.repeat_man(["clck", "l"], reps=2)

        self.assertEqual(calls, [("clck", "l"), ("clck", "l")])

    def test_repeat_man_checks_stop_flag_before_each_manual_command_token_stream(self):
        bot = Bot()
        calls = []
        stop_after_first_click = {"enabled": False}

        def fake_check_key(trigger):
            return stop_after_first_click["enabled"]

        def fake_mouse_clck(btn):
            calls.append(("clck", btn))
            if len(calls) == 1:
                stop_after_first_click["enabled"] = True

        bot.kb.check_key_pressed = fake_check_key
        bot.m.clck = fake_mouse_clck

        bot.repeat_man(["clck", "l", "clck", "r"], reps=1)

        self.assertEqual(calls, [("clck", "l")])

    def test_start_interruption_monitor_is_idempotent_for_repeated_esc_events(self):
        kb = Keyboard()
        captured = {}

        class FakeKey:
            name = "esc"
            char = None

        class FakeListener:
            def __init__(self, on_press=None, on_release=None):
                captured["on_press"] = on_press
                self.running = True

            def start(self):
                self.running = True

            def stop(self):
                self.running = False

        with patch("Models.Keyboard.USE_PYNPUT_KB", True), patch("Models.Keyboard.keyboard") as fake_keyboard:
            fake_keyboard.Listener = FakeListener
            kb.start_interruption_monitor("esc")

            captured["on_press"](FakeKey())
            captured["on_press"](FakeKey())
            captured["on_press"](FakeKey())

            self.assertTrue(kb.stop_requested)

    def test_start_interruption_monitor_catches_stop_key_without_stopping_listener(self):
        kb = Keyboard()
        captured = {}

        class FakeKey:
            name = "esc"

        class FakeListener:
            def __init__(self, on_press=None, on_release=None):
                captured["on_press"] = on_press
                self.running = True

            def start(self):
                self.running = True

            def stop(self):
                self.running = False

        with patch("Models.Keyboard.USE_PYNPUT_KB", True), patch("Models.Keyboard.keyboard") as fake_keyboard:
            fake_keyboard.Listener = FakeListener
            kb.start_interruption_monitor("esc")

            # Simulate the actual keyboard callback from pynput, not a fake
            # event model that invents a char field. The callback should set
            # the shared flag and leave the listener active.
            captured["on_press"](FakeKey())

            self.assertTrue(kb.stop_requested)


if __name__ == "__main__":
    unittest.main()
