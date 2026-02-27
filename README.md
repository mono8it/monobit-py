# monobit-py

Lightweight Python SDK for capturing and sending structured exception events to a Monobit ingest server.

`monobit-py` automatically captures unhandled exceptions and allows manual exception reporting with rich stack trace context.

---

## Features

- Automatic capture of unhandled exceptions
- Manual exception capture
- Thread exception support (Python 3.8+)
- Structured stack traces
- Code context (with exact exception line)
- Runtime & system metadata
- Secure ingestion via `X-MONOBIT-KEY` header

---

## Installation

### Development (Editable Mode)

```bash
pip install -e /path/to/monobit-py
```

### From PyPI (future release)

```bash
pip install monobit-py
```

---

## Basic Usage

```python
from monobit import Monobit

client = Monobit(
    ingest_key="sk_live_123",
    ingest_url="http://127.0.0.1:8000/ingest/",
    service_details={
        "name": "billing-api",
        "version": "1.0.0"
    }
)

# Enable automatic global exception capture
client.init()

# This will automatically be captured and sent
1 / 0
```

---

## Manual Capture

```python
try:
    1 / 0
except Exception as e:
    client.capture_exception(e)
```

---

## Configuration

### Required Parameters

- `ingest_key` – Secret ingest key (sent via `X-MONOBIT-KEY` header)
- `ingest_url` – Ingest endpoint URL

### Optional Parameters

- `service_details` – Dict containing service metadata:

```python
{
    "name": "service-name",
    "version": "1.0.0"
}
```

---

## What Gets Captured

Each event includes:

- Unique `occurrence_id`
- Timestamp (UTC)
- SDK version
- Runtime info (Python version)
- System info (OS, architecture, hostname)
- Process info (PID, thread)
- Full structured stack trace
- Code context around exception line

---

## Security

The ingest key is sent via HTTP header:

X-MONOBIT-KEY: <your_key>

It is **not included in the payload**.

---

## License
