import time
import os
import json
from urllib.request import Request, urlopen
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from avatars.base_avatar import BaseAvatar
from utils.logger import logger

def _send_streamed_text(chunks, avatar_session, datainfo, start):
    """Batch streamed LLM text into short, speakable clauses."""
    result = ""
    first = True
    for msg in chunks:
        if not msg:
            continue
        if first:
            logger.info(f"llm Time to first chunk: {time.perf_counter() - start}s")
            first = False
        lastpos = 0
        for i, char in enumerate(msg):
            if char in ",.!;:，。！？：；":
                result += msg[lastpos:i + 1]
                lastpos = i + 1
                if len(result) > 10:
                    logger.info(result)
                    avatar_session.put_msg_txt(result, datainfo)
                    result = ""
        result += msg[lastpos:]
    if result:
        avatar_session.put_msg_txt(result, datainfo)


def _ollama_chunks(message):
    base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
    model = os.getenv("OLLAMA_MODEL", "ornith:latest")
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "你是一个知识助手，尽量以简短、口语化的方式输出。"},
            {"role": "user", "content": message},
        ],
        "stream": True,
    }).encode("utf-8")
    request = Request(
        f"{base_url}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=120) as response:
        for line in response:
            if not line.strip():
                continue
            event = json.loads(line)
            yield event.get("message", {}).get("content", "")


def llm_response(message,avatar_session:'BaseAvatar',datainfo:dict={}):
    try:
        start = time.perf_counter()
        if os.getenv("LLM_PROVIDER", "dashscope").lower() == "ollama":
            model = os.getenv("OLLAMA_MODEL", "ornith:latest")
            logger.info(f"llm provider=ollama model={model}")
            _send_streamed_text(_ollama_chunks(message), avatar_session, datainfo, start)
            logger.info(f"llm Time to last chunk: {time.perf_counter() - start}s")
            return

        from openai import OpenAI
        client = OpenAI(
            # 如果您没有配置环境变量，请在此处用您的API Key进行替换
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            # 填写DashScope SDK的base_url
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        end = time.perf_counter()
        logger.info(f"llm Time init: {end-start}s,{message}")
        completion = client.chat.completions.create(
            model="qwen-plus",
            messages=[{'role': 'system', 'content': '你是一个知识助手，尽量以简短、口语化的方式输出'},
                    {'role': 'user', 'content': message}],
            stream=True,
            # 通过以下设置，在流式输出的最后一行展示token使用信息
            stream_options={"include_usage": True}
        )
        _send_streamed_text(
            (chunk.choices[0].delta.content for chunk in completion if chunk.choices),
            avatar_session,
            datainfo,
            start,
        )
        logger.info(f"llm Time to last chunk: {time.perf_counter() - start}s")
        
    except Exception as e:
        logger.exception('llm exceptiopn:')
        return
