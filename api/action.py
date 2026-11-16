from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime, timezone

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            payload = json.loads(body) if body else {}
            if not isinstance(payload, dict):
                payload = {}
        except (json.JSONDecodeError, UnicodeDecodeError):
            payload = {}

        action = payload.get("action", "POLICY_ENFORCEMENT")
        target = payload.get("target", "ALL_ENDPOINTS")

        response = {
            "status": "SUCCESS",
            "action": action,
            "target": target,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "latency_ms": 138,
            "message": (
                f"Simulated execution of {action} on target {target}. "
                "No real banking infrastructure was affected."
            )
        }

        body = json.dumps(response).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
