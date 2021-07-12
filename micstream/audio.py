import logging
import os
import signal
import subprocess
import sys
import time


class AudioSource:
    def __init__(self,
                 device: str,
                 audio_system: str = 'alsa',
                 sample_rate: int = 44100,
                 bitrate: int = 128,
                 channels: int = 1,
                 ffmpeg_bin: str = 'ffmpeg',
                 bufsize: int = 8192,
                 debug: bool = False):
        self.ffmpeg_bin = ffmpeg_bin
        self.debug = debug
        self.bufsize = bufsize
        self.devnull = None
        self.ffmpeg = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG if self.debug else logging.INFO)
        self.ffmpeg_args = (
            ffmpeg_bin, '-f', audio_system, '-i', device, '-vn', '-acodec', 'libmp3lame',
            '-b:a', str(bitrate) + 'k', '-ac', str(channels), '-ar', str(sample_rate),
            '-f', 'mp3', '-')

# For those of you who have a mono (1 channel) mic, the '-ac' flag should be entered strictly
# before the '-i device'; if that flag is set after the device declaration, then the setting
# will apply for the output (as per the man page for ffmepg command). Hope this helps.
# Ultimatelly, it will look like this:
#
#         self.ffmpeg_args = (
#            ffmpeg_bin, '-f', audio_system, '-ac', '1', '-i', device, '-vn', '-acodec', 'libmp3lame',
#            '-b:a', str(bitrate) + 'k', '-ac', str(channels), '-ar', str(sample_rate),
#            '-f', 'mp3', '-')
#


        self._ffmpeg_start_time = None
        self._first_sample_time = None
        self.latency = 0.

    def __iter__(self):
        return self

    def __next__(self) -> bytes:
        if not self.ffmpeg or self.ffmpeg.poll() is not None:
            raise StopIteration

        while True:
            data = self.ffmpeg.stdout.read(self.bufsize)
            if not data:
                break

            if not self._first_sample_time:
                self._first_sample_time = time.time()
                self.latency = self._first_sample_time - self._ffmpeg_start_time
                self.logger.info('Estimated latency: {} msec'.format(int(self.latency * 1000)))

            if time.time() - self._first_sample_time >= self.latency:
                return data

        raise StopIteration

    def __enter__(self):
        kwargs = dict(stdout=subprocess.PIPE)
        if not self.debug:
            self.devnull = open(os.devnull, 'w')
            kwargs['stderr'] = self.devnull

        self.logger.info('Running FFmpeg: {}'.format(' '.join(self.ffmpeg_args)))
        self.ffmpeg = subprocess.Popen(self.ffmpeg_args, **kwargs)
        self._ffmpeg_start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.ffmpeg:
            self.ffmpeg.terminate()
            try:
                self.ffmpeg.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.logger.warning('FFmpeg process termination timeout')

            if self.ffmpeg.poll() is None:
                self.ffmpeg.kill()

            self.ffmpeg.wait()
            self.ffmpeg = None

        if self.devnull:
            self.devnull.close()
            self.devnull = None

        self._ffmpeg_start_time = None
        self._first_sample_time = None

    def pause(self):
        if not self.ffmpeg:
            return

        self.ffmpeg.send_signal(signal.SIGSTOP)

    def resume(self):
        if not self.ffmpeg:
            return

        self.ffmpeg.send_signal(signal.SIGCONT)


# vim:sw=4:ts=4:et:
