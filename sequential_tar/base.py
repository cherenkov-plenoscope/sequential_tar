import tarfile
import io
import gzip


def open(path, mode):
    """
    Read or write tar files in a sequential way without seeking.

    Parameters
    ----------
    path : str
        Path to file.
    mode : str
        Either of ['r', 'r|gz', 'w', 'w|gz']. The 't' for text can be added but
        is ignored.

    Returns
    -------
    reader/writer : Reader/Writer
        Depending on mode.
    """
    if "r" in mode:
        return SequentialTarReader(path=path, mode=mode)
    elif "w" in mode:
        return SequentialTarWriter(path=path, mode=mode)
    else:
        raise ValueError("mode must either contain 'r' or 'w'.")


def tarf_write(tarf, filename, payload, mode="wt"):
    if "b" in mode:
        payload_raw = payload
    elif "t" in mode:
        payload_raw = str.encode(payload)
    else:
        raise ValueError("mode must either contain 'b' or 't'.")

    if "|gz" in mode:
        payload_bytes = gzip.compress(payload_raw)
    else:
        payload_bytes = payload_raw

    TAR_BLOCK_SIZE = 512
    SIZE_WRITTEN = TAR_BLOCK_SIZE

    with io.BytesIO() as buff:
        tarinfo = tarfile.TarInfo(filename)
        tarinfo.size = buff.write(payload_bytes)
        SIZE_WRITTEN += tarinfo.size
        buff.seek(0)
        tarf.addfile(tarinfo, buff)
    return SIZE_WRITTEN


class TarItem:
    def __init__(self, filename, raw):
        self.filename = filename
        self.raw = raw

    def read(self, mode="rb"):
        assert "r" in mode
        assert not "w" in mode

        if "|gz" in mode:
            payload = gzip.decompress(self.raw)
        else:
            payload = self.raw

        if "b" in mode:
            out = payload
        elif "t" in mode:
            out = bytes.decode(payload)
        else:
            raise ValueError("mode must either contain 'b' or 't'.")

        return out


class SequentialTarWriter:
    def __init__(self, path, mode):
        self.path = path
        self.mode = mode
        self.tarf = tarfile.open(name=self.path, mode=mode)

    def write(self, filename=None, payload=None, mode="wb"):
        return tarf_write(
            tarf=self.tarf,
            filename=filename,
            payload=payload,
            mode=mode,
        )

    def close(self):
        self.tarf.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def __repr__(self):
        out = "{:s}(path='{:s}', mode='{:s}')".format(
            self.__class__.__name__, self.path.path, self.mode
        )
        return out


class SequentialTarReader:
    def __init__(self, path, mode):
        self.path = path
        self.mode = mode
        self.tarf = tarfile.open(name=self.path, mode=mode)

    def next(self):
        return self.__next__()

    def __next__(self):
        tarinfo = self.tarf.next()
        if tarinfo is None:
            raise StopIteration
        raw = self.tarf.extractfile(tarinfo).read()
        return TarItem(filename=tarinfo.name, raw=raw)

    def __iter__(self):
        return self

    def close(self):
        self.tarf.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def __repr__(self):
        out = "{:s}(path='{:s}', mode='{:s}')".format(
            self.__class__.__name__, self.path.path, self.mode
        )
        return out
