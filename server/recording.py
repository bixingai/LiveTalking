import os


def recording_file_ready(path: str) -> bool:
    return os.path.isfile(path)


def stop_result(was_recording: bool, output_path: str, finalize) -> bool:
    if was_recording:
        finalize()
    return recording_file_ready(output_path)


def end_record_body(file_exists: bool) -> dict:
    return {"code": 0, "msg": "ok", "data": {"ready": bool(file_exists)}}
