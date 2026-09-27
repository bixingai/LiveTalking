import json
import os
import tempfile
import unittest

from server.recording import end_record_body, recording_file_ready, stop_result


class RecordingReadyTests(unittest.TestCase):
    def test_missing_file_is_not_ready_and_hides_the_path(self):
        body = end_record_body(recording_file_ready(os.path.join(tempfile.gettempdir(), "missing-record.mp4")))
        self.assertEqual(body["data"], {"ready": False})
        self.assertNotIn("data/record", json.dumps(body))
        self.assertNotIn("mp4", json.dumps(body["data"]))

    def test_existing_file_is_ready(self):
        handle = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        handle.close()
        try:
            body = end_record_body(recording_file_ready(handle.name))
            self.assertEqual(body["data"]["ready"], True)
            self.assertNotIn(handle.name, json.dumps(body))
            called = {"finalize": False}

            def finalize():
                called["finalize"] = True

            self.assertTrue(stop_result(False, handle.name, finalize))
            self.assertFalse(called["finalize"])
        finally:
            os.remove(handle.name)


if __name__ == "__main__":
    unittest.main()
