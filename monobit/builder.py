import uuid
import datetime
import traceback
import linecache
import sys
import platform
import socket
import os
import threading


def build_error_event(
    e: Exception,
    service_details: dict,
    sdk_version: str,
    context_lines: int = 5,
) -> dict:

    tb = traceback.extract_tb(e.__traceback__)
    frames = []

    for frame in tb:
        filename = frame.filename
        lineno = frame.lineno

        start = max(1, lineno - context_lines)
        end = lineno + context_lines

        code_context = []

        for i in range(start, end + 1):
            line = linecache.getline(filename, i)
            if line:
                code_context.append(
                    {
                        "lineno": i,
                        "content": line.rstrip(),
                        "is_exception_line": i == lineno,
                    }
                )

        frames.append(
            {
                "filename": filename,
                "function": frame.name,
                "lineno": lineno,
                "code_context": code_context,
            }
        )

    return {
        "occurrence_id": uuid.uuid4().hex,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "sdk": {
            "name": "monobit-py",
            "version": sdk_version,
        },
        "environment": os.getenv("APP_ENV", "development"),
        "service": service_details or {},
        "runtime": {
            "name": "python",
            "version": sys.version.split()[0],
        },
        "system": {
            "os": platform.system(),
            "os_version": platform.release(),
            "architecture": platform.machine(),
            "hostname": socket.gethostname(),
        },
        "process": {
            "pid": os.getpid(),
            "thread": threading.current_thread().name,
        },
        "exception": {
            "type": type(e).__name__,
            "message": str(e),
            "frames": frames,
        },
    }
