import asyncio
import json
import sys
import threading
import types
import unittest

from aiohttp import web

fake_base = types.ModuleType("avatars.base_avatar")
fake_base.BaseAvatar = object
sys.modules.setdefault("avatars.base_avatar", fake_base)

fake_aiortc = types.ModuleType("aiortc")
fake_aiortc.RTCPeerConnection = object
fake_aiortc.RTCSessionDescription = object
fake_aiortc.RTCIceServer = object
fake_aiortc.RTCConfiguration = object
sys.modules.setdefault("aiortc", fake_aiortc)
fake_sender = types.ModuleType("aiortc.rtcrtpsender")
fake_sender.RTCRtpSender = object
sys.modules.setdefault("aiortc.rtcrtpsender", fake_sender)

from server.routes import close_session, setup_routes
from server.rtc_manager import RTCManager
from server.session_manager import SessionClosedError, session_manager


class FakeAvatar:
    def __init__(self):
        self.quit_event = threading.Event()
        self.recording = False
        self.flushed = False

    def stop_recording(self):
        self.recording = False

    def flush_talk(self):
        self.flushed = True


class FakePeer:
    def __init__(self):
        self.closed = False
        self.connectionState = "connected"

    async def close(self):
        self.closed = True
        self.connectionState = "closed"


class CloseSessionTests(unittest.TestCase):
    def setUp(self):
        session_manager.sessions.clear()
        session_manager.set_max_session(1)
        session_manager.init_builder(lambda sessionid, params: FakeAvatar())
        self.manager = RTCManager(type("Opt", (), {"stun": "stun:example"})())

    def tearDown(self):
        session_manager.sessions.clear()

    def test_close_removes_the_session_and_frees_the_slot(self):
        async def scenario():
            sessionid = await session_manager.create_session({"avatar": "demo"})
            avatar = session_manager.get_session(sessionid)
            avatar.recording = True
            peer = FakePeer()
            self.manager.session_pcs[sessionid] = peer
            self.manager.pcs.add(peer)

            app = web.Application()
            app["rtc_manager"] = self.manager
            setup_routes(app)
            request = type("Request", (), {})()
            request.app = app

            async def body():
                return {"sessionid": sessionid}

            request.json = body
            response = await close_session(request)
            self.assertEqual(response.status, 200)
            self.assertEqual(json.loads(response.text)["code"], 0)
            self.assertIsNone(session_manager.get_session(sessionid))
            self.assertNotIn(sessionid, self.manager.session_pcs)
            self.assertTrue(peer.closed)
            self.assertFalse(avatar.recording)
            self.assertTrue(avatar.quit_event.is_set())
            self.assertTrue(avatar.flushed)

            missing = type("Request", (), {})()
            missing.app = app

            async def missing_body():
                return {"sessionid": sessionid}

            missing.json = missing_body
            not_found = await close_session(missing)
            self.assertEqual(not_found.status, 404)
            self.assertNotIn("Traceback", not_found.text)

            again = await session_manager.create_session({"avatar": "demo"})
            self.assertTrue(session_manager.has_session(again))

            rejected = type("Request", (), {})()
            rejected.app = app

            async def extra():
                return {"sessionid": again, "text": "hello"}

            rejected.json = extra
            bad = await close_session(rejected)
            self.assertEqual(json.loads(bad.text)["msg"], "sessionid is required")
            self.assertTrue(session_manager.has_session(again))

        asyncio.run(scenario())

    def test_close_during_build_is_not_replaced(self):
        started = threading.Event()
        release = threading.Event()

        def build(sessionid, params):
            started.set()
            release.wait(3)
            return FakeAvatar()

        session_manager.init_builder(build)

        async def scenario():
            task = asyncio.create_task(session_manager.create_session({}, "fixed-id"))
            await asyncio.to_thread(started.wait)
            self.assertTrue(await self.manager.close_session("fixed-id"))
            release.set()
            with self.assertRaises(SessionClosedError):
                await task
            self.assertNotIn("fixed-id", session_manager.sessions)

        asyncio.run(scenario())


if __name__ == "__main__":
    unittest.main()
