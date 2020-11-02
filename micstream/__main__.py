import argparse
import logging
import sys

from micstream import AudioSource, Server


def init_logging():
    logging.basicConfig(level=logging.INFO,
                        stream=sys.stdout,
                        format='[%(asctime)s] %(name)s|%(levelname)-8s|%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')


def get_args():
    parser = argparse.ArgumentParser(description='Stream an audio source over HTTP as mp3')
    parser.add_argument('-d', '--device', help='ALSA/Pulse device ID/name', required=True, dest='device')
    parser.add_argument('-s', '--sound-system', help='Sound system. Supported: alsa, pulse. Default: alsa', required=False, default='alsa', dest='audio_system')
    parser.add_argument('-v', '--verbose', help='Verbose/debug mode', required=False, action='store_true', dest='debug')
    parser.add_argument('-a', '--address', help='Bind address (default: 0.0.0.0)', required=False, default='0.0.0.0', dest='address')
    parser.add_argument('-p', '--port', help='HTTP listen port (default: 8080)', required=False, default=8080, type=int, dest='port')
    parser.add_argument('-e', '--endpoint', help='HTTP endpoint for streaming (default: /stream.mp3)', required=False, default='/stream.mp3', dest='endpoint')
    parser.add_argument('-r', '--sample-rate', help='Recording sample rate (default: 44100)', required=False, default=44100, type=int, dest='sample_rate')
    parser.add_argument('-b', '--bitrate', help='mp3 compression bitrate, in kbps (default: 128)', required=False, default=128, type=int, dest='bitrate')
    parser.add_argument('-c', '--channels', help='Number of recording channels (default: 1)', required=False, default=1, type=int, dest='channels')
    parser.add_argument('-f', '--ffmpeg', help='Path to the FFmpeg binary (default: ffmpeg)', required=False, default='ffmpeg', dest='ffmpeg_bin')
    parser.add_argument('-B', '--bufsize', help='Size of the audio chunks to be delivered to the server (default: 8192 bytes)', required=False, default=8192, type=int, dest='bufsize')
    opts, _ = parser.parse_known_args(sys.argv[1:])
    return opts


def main():
    init_logging()
    args = get_args()

    with AudioSource(device=args.device,
                     audio_system=args.audio_system,
                     sample_rate=args.sample_rate,
                     bitrate=args.bitrate,
                     channels=args.channels,
                     ffmpeg_bin=args.ffmpeg_bin,
                     bufsize=args.bufsize,
                     debug=args.debug) as source, \
         Server(host=args.address,
                port=args.port,
                endpoint=args.endpoint,
                debug=args.debug) as server:
        for sample in source:
            server.process_audio(sample)


if __name__ == '__main__':
    main()


# vim:sw=4:ts=4:et:
