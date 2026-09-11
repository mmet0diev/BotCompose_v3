import unittest

from Models.Bot import Bot


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


if __name__ == "__main__":
    unittest.main()
