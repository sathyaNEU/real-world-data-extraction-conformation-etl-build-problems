"""task470: the meter data hub's hourly extract written as the hub exports it, a plain parquet file with no writer
name: no pandas or Arrow schema in the key-value metadata and no created_by in the footer."""
import pyarrow as pa
import pyarrow.parquet as pq


def write(df, path, **kw):
    t = pa.Table.from_pandas(df, preserve_index=False).replace_schema_metadata(None)
    pq.write_table(t, path, store_schema=False, **kw)
    _drop_created_by(path)


def _varint(b, i):
    v = s = 0
    while True:
        c = b[i]; i += 1
        v |= (c & 0x7F) << s; s += 7
        if not c & 0x80:
            return v, i


def _skip(b, i, t):
    """Skip one compact-protocol thrift value of type t starting at b[i]."""
    if t in (1, 2):
        return i
    if t == 3:
        return i + 1
    if t in (4, 5, 6):
        return _varint(b, i)[1]
    if t == 7:
        return i + 8
    if t == 8:
        n, i = _varint(b, i)
        return i + n
    if t in (9, 10):
        h = b[i]; i += 1
        n, et = h >> 4, h & 0x0F
        if n == 15:
            n, i = _varint(b, i)
        for _ in range(n):
            i = i + 1 if et in (1, 2) else _skip(b, i, et)
        return i
    if t == 11:
        n, i = _varint(b, i)
        if n:
            kv = b[i]; i += 1
            for _ in range(n):
                i = _skip(b, i, kv >> 4)
                i = _skip(b, i, kv & 0x0F)
        return i
    if t == 12:
        while True:
            h = b[i]; i += 1
            if h == 0:
                return i
            if not h >> 4:
                i = _varint(b, i)[1]
            i = _skip(b, i, h & 0x0F)
    raise ValueError("thrift type %d" % t)


def _drop_created_by(path):
    """The market-data export carries no writer name: FileMetaData field 6 (created_by) is left out of the footer,
    as the format allows, and the next field's header is re-based on the field before it."""
    raw = open(path, "rb").read()
    assert raw[-4:] == b"PAR1"
    n = int.from_bytes(raw[-8:-4], "little")
    meta, body = raw[-8 - n:-8], raw[:-8 - n]
    out, i, last, prev, dropped = bytearray(), 0, 0, 0, False
    while meta[i]:
        h, j = meta[i], i + 1
        if h >> 4:
            fid = last + (h >> 4)
        else:
            z, j = _varint(meta, j)
            fid = (z >> 1) ^ -(z & 1)
        t = h & 0x0F
        end = _skip(meta, j, t)
        if fid == 6:
            dropped = True
        else:
            out += bytes([((fid - prev) << 4) | t]) if 0 < fid - prev <= 15 else bytes([t]) + _zz(fid)
            out += meta[j:end]
            prev = fid
        last, i = fid, end
    out += meta[i:]
    assert dropped, "no created_by in the footer"
    open(path, "wb").write(body + bytes(out) + len(out).to_bytes(4, "little") + b"PAR1")


def _zz(v):
    z, o = (v << 1) ^ (v >> 63), bytearray()
    while True:
        if z < 0x80:
            o.append(z)
            return bytes(o)
        o.append((z & 0x7F) | 0x80); z >>= 7
