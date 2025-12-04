use core::slice;
use std::ffi::{c_char, CStr, CString};
use std::fs;

#[unsafe(no_mangle)]
pub extern "C" fn letter_grid_file(
    path: *const c_char,
    separator: *const c_char,
    out_buf: *mut u8,
    out_rows: *mut usize,
    out_cols: *mut usize,
) {
    let c_str = unsafe { CStr::from_ptr(path) };
    let path_str = c_str.to_str().unwrap();
    let content = fs::read_to_string(path_str).unwrap();
    let trimmed = content.trim();
    let lines_c: Vec<CString> = trimmed.lines().map(|r| CString::new(r).unwrap()).collect();
    let lines_ptrs: Vec<*const c_char> = lines_c.iter().map(|s| s.as_ptr()).collect();

    letter_grid(
        lines_ptrs.as_ptr(),
        lines_ptrs.len(),
        separator,
        out_buf,
        out_rows,
        out_cols
    );
}

#[unsafe(no_mangle)]
pub extern "C" fn number_grid_file(
    path: *const c_char,
    separator: *const c_char,
    out_buf: *mut i64,
    out_rows: *mut usize,
    out_cols: *mut usize,
) {
    let c_str = unsafe { CStr::from_ptr(path) };
    let path_str = c_str.to_str().unwrap();
    let content = fs::read_to_string(path_str).unwrap();
    let trimmed = content.trim();
    let lines_c: Vec<CString> = trimmed.lines().map(|r| CString::new(r).unwrap()).collect();
    let lines_ptrs: Vec<*const c_char> = lines_c.iter().map(|s| s.as_ptr()).collect();

    number_grid(
        lines_ptrs.as_ptr(),
        lines_ptrs.len(),
        separator,
        out_buf,
        out_rows,
        out_cols
    );
}

#[unsafe(no_mangle)]
pub extern "C" fn letter_grid(
    lines_ptr: *const *const c_char,
    n_lines: usize,
    separator: *const c_char,
    out_buf: *mut u8,
    out_rows: *mut usize,
    out_cols: *mut usize,
) {
    let sep = unsafe { CStr::from_ptr(separator).to_str().unwrap() };
    let lines: Vec<&str> = unsafe {
        slice::from_raw_parts(lines_ptr, n_lines)
            .iter()
            .map(|&p| CStr::from_ptr(p).to_str().unwrap())
            .collect()
    };

    let grid = lines.iter().map(|line| {
        if sep.is_empty() {
            line.chars().collect::<Vec<char>>()
        } else {
            line.split(sep).map(|s| s.chars().next().unwrap_or(' ')).collect()
        }
    }).collect::<Vec<Vec<char>>>();

    let rows = grid.len();
    let cols = grid.get(0).map(|r| r.len()).unwrap_or(0);

    unsafe {
        *out_rows = rows;
        *out_cols = cols;
        for r in 0..rows {
            for c in 0..cols {
                *out_buf.add(r * cols + c) = grid[r][c] as u8;
            }
        }
    }
}

#[unsafe(no_mangle)]
pub extern "C" fn number_grid(
    lines_ptr: *const *const c_char,
    n_lines: usize,
    separator: *const c_char,
    out_buf: *mut i64,
    out_rows: *mut usize,
    out_cols: *mut usize,
) {
    let sep = unsafe { CStr::from_ptr(separator).to_str().unwrap() };
    let lines: Vec<&str> = unsafe {
        slice::from_raw_parts(lines_ptr, n_lines)
            .iter()
            .map(|&p| CStr::from_ptr(p).to_str().unwrap())
            .collect()
    };

    let grid = lines.iter().map(|line| {
        if sep.is_empty() {
            line.chars().map(|c| c.to_digit(10).unwrap() as i64).collect::<Vec<i64>>()
        } else {
            line.split(sep).map(|s| s.parse::<i64>().unwrap()).collect()
        }
    }).collect::<Vec<Vec<i64>>>();

    let rows = grid.len();
    let cols = grid.get(0).map(|r| r.len()).unwrap_or(0);

    unsafe {
        *out_rows = rows;
        *out_cols = cols;
        for r in 0..rows {
            for c in 0..cols {
                *out_buf.add(r * cols + c) = grid[r][c];
            }
        }
    }
}
