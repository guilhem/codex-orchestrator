import json
from pathlib import Path
import sys


try:
    payload = json.load(sys.stdin)
except (ValueError, UnicodeError):
    payload = None

if (isinstance(payload, dict)
        and payload.get('hook_event_name') == 'UserPromptSubmit'
        and 'agent_id' not in payload
        and 'agent_type' not in payload):
    sys.stdout.buffer.write((Path(__file__).resolve().parents[1] / 'hooks/prompt-reminder.txt').read_bytes())
