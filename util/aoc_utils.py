from cffi import FFI
import numpy as np
import itertools
import os

# Globals
alphabet = "abcdefghijklmnopqrstuvwxyz"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# All 3x3 neighbor directions including diagonals
ds = itertools.product([-1, 0, 1], [-1, 0, 1])

ffi = FFI()

ffi.cdef("""
    int find_grid(
        const long long *grid, size_t grid_h, size_t grid_w,
        const long long *pat, size_t pat_h, size_t pat_w,
        size_t *out_x, size_t *out_y
    );

    size_t find_all_grid(
        const long long *grid, size_t grid_h, size_t grid_w,
        const long long *pat, size_t pat_h, size_t pat_w,
        size_t *out_ptr, size_t max_out
    );

    void letter_grid_file(
        const char *path,
        const char *separator,
        char *out_buf, size_t *out_rows, size_t *out_cols
    );

    void number_grid_file(
        const char *path,
        const char *separator,
        int64_t *out_buf, size_t *out_rows, size_t *out_cols
    );

    void letter_grid(
        const char **lines,
        size_t n_lines,
        const char *separator,
        char *out_buf, size_t *out_rows, size_t *out_cols
    );

    void number_grid(
        const char **lines,
        size_t n_lines,
        const char *separator,
        int64_t *out_buf, size_t *out_rows, size_t *out_cols
    );
""")

lib = ffi.dlopen(os.path.join(os.path.dirname(__file__), "libaoc_utils.dylib"))

def find_grid(grid: np.ndarray, pattern: np.ndarray):
    grid = np.ascontiguousarray(grid, dtype=np.int64)
    pattern = np.ascontiguousarray(pattern, dtype=np.int64)

    out_x = ffi.new("size_t *")
    out_y = ffi.new("size_t *")

    ok = lib.find_grid(
        ffi.cast("long long *", grid.ctypes.data),
    grid.shape[0], grid.shape[1],
        ffi.cast("long long *", pattern.ctypes.data),
        pattern.shape[0], pattern.shape[1],
        out_x, out_y
    )

    if ok:
        return int(out_x[0]), int(out_y[0])
    return None

def find_all_grid(grid: np.ndarray, pattern: np.ndarray, max_matches=1000):
    grid = np.ascontiguousarray(grid, dtype=np.int64)
    pattern = np.ascontiguousarray(pattern, dtype=np.int64)

    out_buf = ffi.new(f"size_t[{max_matches * 2}]")
    n_matches = lib.find_all_grid(
        ffi.cast("long long *", grid.ctypes.data),
        grid.shape[0], grid.shape[1],
        ffi.cast("long long *", pattern.ctypes.data),
        pattern.shape[0], pattern.shape[1],
        out_buf,
        max_matches
    )

    matches = [(int(out_buf[i*2]), int(out_buf[i*2+1])) for i in range(n_matches)]
    return matches

def letter_grid_file(path, separator="", buf_size=10_000):
    out_buf = ffi.new("char[]", buf_size)
    out_rows = ffi.new("size_t *")
    out_cols = ffi.new("size_t *")
    path_c = ffi.new("char[]", path.encode("utf-8"))
    sep_c = ffi.new("char[]", separator.encode("utf-8"))

    lib.letter_grid_file(path_c, sep_c, out_buf, out_rows, out_cols)
    rows, cols = out_rows[0], out_cols[0]
    return [[out_buf[r*cols + c].decode('utf-8') for c in range(cols)] for r in range(rows)]

def number_grid_file(path, separator="", buf_size=10_000):
    out_buf = ffi.new("int32_t[]", buf_size)
    out_rows = ffi.new("size_t *")
    out_cols = ffi.new("size_t *")
    path_c = ffi.new("char[]", path.encode("utf-8"))
    sep_c = ffi.new("char[]", separator.encode("utf-8"))

    lib.number_grid_file(path_c, sep_c, out_buf, out_rows, out_cols)
    rows, cols = out_rows[0], out_cols[0]
    return [[out_buf[r*cols + c] for c in range(cols)] for r in range(rows)]

def letter_grid(lines, separator="", buf_size=10_000):
    out_buf = ffi.new("uint8_t[]", buf_size)
    out_rows = ffi.new("size_t *")
    out_cols = ffi.new("size_t *")
    nlines = len(lines)
    sep_c = ffi.new("char[]", separator.encode("utf-8"))
    lines_c = [ffi.new("char[]", s.encode("utf-8")) for s in lines]
    lines_c_ptrs = ffi.new("char*[]", lines_c)

    lib.letter_grid(lines_c_ptrs, nlines, sep_c, out_buf, out_rows, out_cols)
    rows, cols = out_rows[0], out_cols[0]
    return [[out_buf[r*cols + c] for c in range(cols)] for r in range(rows)]

def number_grid(lines, separator="", buf_size=10_000):
    out_buf = ffi.new("int64_t[]", buf_size)
    out_rows = ffi.new("size_t *")
    out_cols = ffi.new("size_t *")
    nlines = len(lines)
    sep_c = ffi.new("char[]", separator.encode("utf-8"))
    lines_c = [ffi.new("char[]", s.encode("utf-8")) for s in lines]
    lines_c_ptrs = ffi.new("char*[]", lines_c)

    lib.number_grid(lines_c_ptrs, nlines, sep_c, out_buf, out_rows, out_cols)
    rows, cols = out_rows[0], out_cols[0]
    return [[out_buf[r*cols + c] for c in range(cols)] for r in range(rows)]
