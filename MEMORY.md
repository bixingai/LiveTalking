# LiveTalking memory

This repository stays a replaceable GPU engine. Do not add Teachora, Helpora, or Shopora product behavior to `app.py` or `server/routes.py`.

Those products call `C:\Coding\BixingAI\presenter-gateway`. That adapter is a separate internal process with no product UI. Its protocol is not implemented yet. See `docs/presenter-gateway.md`.

Browsers may still open port `5555` in the current local MVPs. That path is temporary.
