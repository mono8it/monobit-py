import requests


class HTTPTransport:
    def __init__(self, ingest_url: str, ingest_key: str):
        self.ingest_url = ingest_url
        self.ingest_key = ingest_key

    def send(self, payload: dict):
        try:
            headers = {
                "Content-Type": "application/json",
                "X-MONOBIT-KEY": self.ingest_key,
            }

            requests.post(
                self.ingest_url,
                json=payload,
                headers=headers,
                timeout=5,
            )
        except Exception:
            # Never crash host app because telemetry failed
            pass
