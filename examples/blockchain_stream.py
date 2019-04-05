import sys
import traceback
import json

import aergo.herapy as herapy

from aergo.herapy.utils.converter import convert_bytes_to_hex_str, \
                                         convert_bytes_to_int_str, get_hash


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    print(*args, **kwargs)


def run():
    try:
        aergo = herapy.Aergo()

        print("------ Connect AERGO -----------")
        aergo.connect('localhost:7845')

        print("------ Get Block Meta Stream -----------")
        stream = aergo.receive_block_stream()
        i = 0
        while i < 3:
            block = next(stream)
            print('[{}] block: {}'.format(i, str(block)))
            i += 1

        print("------ Get Block Stream -----------")
        stream = aergo.receive_block_stream()
        i = 0
        while i < 3:
            block = next(stream)
            print('[{}] block: {}'.format(i, str(block)))
            i += 1

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except Exception as e:
        eprint(e)
        traceback.print_exception(*sys.exc_info())


if __name__ == '__main__':
    run()
