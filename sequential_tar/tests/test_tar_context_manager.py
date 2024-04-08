import sequential_tar as seqtar
import tempfile
import os


def test_context():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "test.tar")

        with seqtar.open(path, "w") as tar:
            for i in range(100):
                tar.write(
                    name="{:06d}.txt".format(i),
                    payload="I am file number {:d}.".format(i),
                    mode="wt",
                )

        with seqtar.open(path, "r") as tar:
            for i, item in enumerate(tar):
                assert item.name == "{:06d}.txt".format(i)

        with seqtar.open(path, "r") as tar:
            for i in range(100):
                item = tar.next()
                content = item.read("rt")
                assert content == "I am file number {:d}.".format(i)
