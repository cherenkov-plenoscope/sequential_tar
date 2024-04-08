import sequential_tar as seqtar
import tempfile
import os


def test_repr():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "test.tar")

        with seqtar.open(path, "w") as ts:
            assert isinstance(ts, seqtar.SequentialTarWriter)
            assert repr(ts).startswith("SequentialTarWriter(")
            assert repr(ts).endswith(")")
            ts.write(
                name="example.txt.gz", payload="Hello world.", mode="wt|gz"
            )

        with seqtar.open(path, "r") as ts:
            assert isinstance(ts, seqtar.SequentialTarReader)
            assert repr(ts).startswith("SequentialTarReader(")
            assert repr(ts).endswith(")")

            item = ts.next()
            assert isinstance(item, seqtar.SequentialTarItem)
            assert repr(item).startswith("SequentialTarItem(")
            assert repr(item).endswith(")")
