# micstream

Stream an audio input device over HTTP as mp3.

## Requirements

`ffmpeg` and `lame` installed on the system, e.g.:

```bash
[sudo] apt-get install ffmpeg lame
```

## Installation

```bash
[sudo] python setup.py install
```

## Usage

```bash
micstream --help                                              <<<
usage: micstream [-h] -d DEVICE [-s AUDIO_SYSTEM] [-v] [-a ADDRESS] [-p PORT] [-e ENDPOINT] [-r SAMPLE_RATE] [-b BITRATE]
                 [-c CHANNELS] [-f FFMPEG_BIN] [-B BUFSIZE]

Stream an audio source over HTTP as mp3

optional arguments:
  -h, --help            show this help message and exit
  -d DEVICE, --device DEVICE
                        ALSA/Pulse device ID/name
  -s AUDIO_SYSTEM, --sound-system AUDIO_SYSTEM
                        Sound system. Supported: alsa, pulse. Default: alsa
  -v, --verbose         Verbose/debug mode
  -a ADDRESS, --address ADDRESS
                        Bind address (default: 0.0.0.0)
  -p PORT, --port PORT  HTTP listen port (default: 8080)
  -e ENDPOINT, --endpoint ENDPOINT
                        HTTP endpoint for streaming (default: /stream.mp3)
  -r SAMPLE_RATE, --sample-rate SAMPLE_RATE
                        Recording sample rate (default: 44100)
  -b BITRATE, --bitrate BITRATE
                        mp3 compression bitrate, in kbps (default: 128)
  -c CHANNELS, --channels CHANNELS
                        Number of recording channels (default: 1)
  -f FFMPEG_BIN, --ffmpeg FFMPEG_BIN
                        Path to the FFmpeg binary (default: ffmpeg)
  -B BUFSIZE, --bufsize BUFSIZE
                        Size of the audio chunks to be delivered to the server (default: 8192 bytes)
```

