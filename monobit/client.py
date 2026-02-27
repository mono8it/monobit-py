import sys
import threading
from .builder import build_error_event
from .transport import HTTPTransport
from .__version__ import __version__


class Monobit:
    def __init__(self, ingest_key: str, ingest_url: str, **kwargs):
        self.ingest_key = ingest_key
        self.service_details = kwargs.get("service_details", {})
        self.transport = HTTPTransport(ingest_url, ingest_key)

        self._original_excepthook = None
        self._installed = False

    def init(self):
        if self._installed:
            return

        self._original_excepthook = sys.excepthook
        sys.excepthook = self._handle_uncaught_exception

        self._install_thread_hook()
        self._installed = True

    def capture_exception(self, e: Exception):
        event = build_error_event(
            e=e,
            service_details=self.service_details,
            sdk_version=__version__,
        )
        self.transport.send(event)

    # ---------------- INTERNAL ---------------- #

    def _handle_uncaught_exception(self, exc_type, exc_value, exc_traceback):
        try:
            event = build_error_event(
                e=exc_value,
                service_details=self.service_details,
                sdk_version=__version__,
            )
            self.transport.send(event)
        except Exception:
            pass

        if self._original_excepthook:
            self._original_excepthook(exc_type, exc_value, exc_traceback)

    def _install_thread_hook(self):
        def thread_exception_handler(args):
            self._handle_uncaught_exception(
                args.exc_type,
                args.exc_value,
                args.exc_traceback,
            )

        if hasattr(threading, "excepthook"):
            threading.excepthook = thread_exception_handler
