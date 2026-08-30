"""Minimal reader for Larian LSPK v18 package files (Baldur's Gate 3)."""
import struct
import lz4.block

try:
    import zstandard
except ImportError:
    zstandard = None
import zlib


class PakEntry:
    __slots__ = ("name", "offset", "part", "flags", "size_disk", "size_raw")

    def __init__(self, name, offset, part, flags, size_disk, size_raw):
        self.name = name
        self.offset = offset
        self.part = part
        self.flags = flags
        self.size_disk = size_disk
        self.size_raw = size_raw


def read_entries(pak_path):
    with open(pak_path, "rb") as f:
        magic = f.read(4)
        assert magic == b"LSPK", f"not a LSPK pak: {magic!r}"
        version, = struct.unpack("<I", f.read(4))
        assert version in (15, 16, 18), f"unsupported pak version {version}"
        file_list_offset, file_list_size = struct.unpack("<QI", f.read(12))
        f.seek(file_list_offset)
        num_files, compressed_size = struct.unpack("<II", f.read(8))
        comp = f.read(compressed_size)
        entry_size = 272 if version == 18 else 296
        raw = lz4.block.decompress(comp, uncompressed_size=num_files * entry_size)
        entries = []
        for i in range(num_files):
            off = i * entry_size
            chunk = raw[off:off + entry_size]
            name = chunk[:256].split(b"\x00", 1)[0].decode("utf-8", "replace")
            if version == 18:
                off1, off2, part, flags, sz_disk, sz_raw = struct.unpack(
                    "<IHBBII", chunk[256:272])
                offset = off1 | (off2 << 32)
            else:
                offset, sz_disk, sz_raw, part, flags = struct.unpack(
                    "<QIIIB", chunk[256:277])
            entries.append(PakEntry(name, offset, part, flags, sz_disk, sz_raw))
        return entries


def extract(pak_path, entry):
    assert entry.part == 0, "multi-part pak entry not supported"
    with open(pak_path, "rb") as f:
        f.seek(entry.offset)
        data = f.read(entry.size_disk)
    method = entry.flags & 0x0F
    if method == 0:
        return data
    if method == 1:
        return zlib.decompress(data)
    if method == 2:
        return lz4.block.decompress(data, uncompressed_size=entry.size_raw)
    if method == 3:
        return zstandard.ZstdDecompressor().decompress(data, max_output_size=entry.size_raw)
    raise ValueError(f"unknown compression method {method}")


if __name__ == "__main__":
    import sys
    from collections import Counter

    pak = sys.argv[1]
    entries = read_entries(pak)
    print(f"{len(entries)} entries")
    dirs = Counter("/".join(e.name.split("/")[:5]) for e in entries)
    for d, n in dirs.most_common(30):
        print(f"  {n:6} {d}")
