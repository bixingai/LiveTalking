def mark_text_queued(avatar) -> None:
    avatar._speech_queued = True


def clear_queued_text(avatar) -> None:
    avatar._speech_queued = False


def current_speech_state(avatar) -> str:
    if getattr(avatar, "speaking", False):
        return "speaking"
    if getattr(avatar, "_speech_queued", False):
        return "queued"
    tts = getattr(avatar, "tts", None)
    pending = getattr(tts, "msgqueue", None)
    if pending is not None and not pending.empty():
        return "queued"
    return "idle"


def speaking_payload(avatar) -> dict:
    speaking = bool(getattr(avatar, "speaking", False))
    return {
        "code": 0,
        "msg": "ok",
        "data": speaking,
        "speech_state": current_speech_state(avatar),
    }
