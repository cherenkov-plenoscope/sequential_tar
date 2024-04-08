import sequential_tar as seqtar
import tempfile
import os


def test_context():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "test.tar")

        with seqtar.open(path, "w") as tar:
            tar.write(
                name="1.txt",
                payload="I am text number 1.",
                mode="wt",
            )
            tar.write(
                name="2.txt.gz",
                payload="I am text number 2.",
                mode="wt|gz",
            )
            tar.write(
                name="3.bin.gz",
                payload=b"0123456789",
                mode="wb|gz",
            )
            tar.write(
                name="4.bin",
                payload=b"123-123-123-123-123-123-123",
                mode="wb",
            )

        with seqtar.open(path, "r") as tar:
            item = next(tar)
            assert item.name == "1.txt"
            assert item.read(mode="rt") == "I am text number 1."

            item = next(tar)
            assert item.name == "2.txt.gz"
            assert item.read(mode="rt|gz") == "I am text number 2."

            item = next(tar)
            assert item.name == "3.bin.gz"
            assert item.read(mode="rb|gz") == b"0123456789"

            item = next(tar)
            assert item.name == "4.bin"
            assert item.read(mode="rb") == b"123-123-123-123-123-123-123"
