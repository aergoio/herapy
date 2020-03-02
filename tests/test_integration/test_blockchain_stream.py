def test_blockchain_stream(aergo) -> None:
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
