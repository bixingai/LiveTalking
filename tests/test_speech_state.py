import unittest
from queue import Queue

from server.speech_state import clear_queued_text, current_speech_state, mark_text_queued, speaking_payload


class Avatar:
    def __init__(self):
        self.speaking = False
        self._speech_queued = False
        self.tts = type("TTS", (), {"msgqueue": Queue()})()


class SpeechStateTests(unittest.TestCase):
    def test_text_is_queued_before_audio_and_boolean_stays_false(self):
        avatar = Avatar()
        mark_text_queued(avatar)
        payload = speaking_payload(avatar)
        self.assertEqual(payload["data"], False)
        self.assertEqual(payload["speech_state"], "queued")

    def test_audible_frames_are_speaking_and_clear_the_queue_flag(self):
        avatar = Avatar()
        mark_text_queued(avatar)
        avatar.speaking = True
        avatar._speech_queued = False
        payload = speaking_payload(avatar)
        self.assertEqual(payload["data"], True)
        self.assertEqual(payload["speech_state"], "speaking")

    def test_interrupt_returns_to_idle(self):
        avatar = Avatar()
        mark_text_queued(avatar)
        avatar.tts.msgqueue.put(("hello", {}))
        clear_queued_text(avatar)
        avatar.tts.msgqueue.queue.clear()
        self.assertEqual(current_speech_state(avatar), "idle")
        self.assertEqual(speaking_payload(avatar)["data"], False)


if __name__ == "__main__":
    unittest.main()
