import logging
import threading

from queue import Queue
from typing import Callable, Dict

from flask import Flask, Response


class Endpoint:
    def __init__(self, action):
        self.action = action

    def __call__(self, *args, **kwargs):
        return Response(self.action(*args, **kwargs), status=200, headers={})


class Server:
    def __init__(self,
                 host: str = '0.0.0.0',
                 port: int = 8080,
                 endpoint: str = '/stream.mp3',
                 debug: bool = False):
        self.host = host
        self.port = port
        self.debug = debug
        self.endpoint = endpoint
        self.app = Flask(__name__)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG if self.debug else logging.INFO)

        self._audio_lock = threading.RLock()
        self._stream_queues: Dict[int, Queue] = {}
        self._next_queue_id = 1

        self.add_endpoints()
        self.thread = threading.Thread(target=self.app.run,
            kwargs=dict(host=self.host, port=self.port,
                debug=debug, use_reloader=False))

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # TODO find a clean way to get Flask to stop

    def process_audio(self, audio: bytes):
        with self._audio_lock:
            for q in self._stream_queues.values():
                q.put(audio)

    def add_endpoints(self):
        self.add_endpoint(self.endpoint, self.stream())

    def add_endpoint(self, endpoint: str, handler: Callable):
        self.app.add_url_rule(endpoint, endpoint, handler)

    def _get_feed(self):
        with self._audio_lock:
            queue_id = self._next_queue_id
            self._stream_queues[queue_id] = Queue()
            self._next_queue_id += 1
            q = self._stream_queues[queue_id]

        try:
            while True:
                audio = q.get()
                if not audio:
                    continue

                self.logger.debug('Got audio sample of length {}'.format(len(audio)))
                yield audio
        finally:
            with self._audio_lock:
                del self._stream_queues[queue_id]

    def stream(self):
        def endpoint():
            return Response(self._get_feed(),
                            mimetype='audio/mpeg')

        return endpoint


# vim:sw=4:ts=4:et:
