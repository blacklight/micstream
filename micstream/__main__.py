import logging
import sys

from micstream import AudioSource, Server


def init_logging():
    logging.basicConfig(level=logging.INFO,
                        stream=sys.stdout,
                        format='[%(asctime)s] %(name)s|%(levelname)-8s|%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')


def main():
    init_logging()

    with AudioSource('plughw:3,0') as source, \
         Server() as server:
        for sample in source:
            server.process_audio(sample)


if __name__ == '__main__':
    main()


# vim:sw=4:ts=4:et:
