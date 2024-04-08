import sequential_tar as seqtar
from sequential_tar import tarfile_add_regular_file
import tarfile as buildin_tarfile
import tempfile
import os


def tarfile_add_dir(tarfile, name):
    tarinfo = buildin_tarfile.TarInfo(name)
    tarinfo.type = b"5"
    assert tarinfo.isdir()
    tarfile.addfile(tarinfo)


def test_sequential_reader_only_returns_regular_files():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "test.tar")

        with buildin_tarfile.open(path, "w") as tf:
            tarfile_add_dir(tarfile=tf, name="mydir1")
            tarfile_add_regular_file(
                tarfile=tf,
                name="my_dir1/example.txt",
                payload="Hello World!\n",
                mode="wt",
            )
            tarfile_add_dir(tarfile=tf, name="mydir2")
            tarfile_add_dir(tarfile=tf, name="mydir3")
            tarfile_add_dir(tarfile=tf, name="mydir4")
            tarfile_add_regular_file(
                tarfile=tf,
                name="my_dir4/example.txt",
                payload="Hello World!\n",
                mode="wt",
            )
            tarfile_add_dir(tarfile=tf, name="mydir5")

        content = {}
        with seqtar.open(path, "r") as stf:
            for item in stf:
                content[item.name] = item.read(mode="rt")

        assert len(content) == 2
        assert "my_dir1/example.txt" in content
        assert "my_dir4/example.txt" in content
