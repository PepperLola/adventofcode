use std::sync::{atomic::{AtomicBool, Ordering}, Mutex};
use rayon::prelude::*;

#[inline(always)]
fn pattern_matches(
    grid: &[i64], H: usize, W: usize,
    pattern: &[i64], IH: usize, IW: usize,
    x: usize, y: usize
) -> bool {
    for dy in 0..IH {
        for dx in 0..IW {
            if grid[(y + dy) * W + (x + dx)] != pattern[dy * IW + dx] {
                return false;
            }
        }
    }
    true
}

#[unsafe(no_mangle)]
pub extern "C" fn find_grid(
    grid_ptr: *const i64,
    grid_h: usize,
    grid_w: usize,
    pat_ptr: *const i64,
    pat_h: usize,
    pat_w: usize,
    out_x: *mut usize,
    out_y: *mut usize,
) -> bool {
    let grid = unsafe { std::slice::from_raw_parts(grid_ptr, grid_h * grid_w) };
    let pat = unsafe { std::slice::from_raw_parts(pat_ptr, pat_h * pat_w) };

    if pat_h > grid_h || pat_w > grid_w {
        return false;
    }

    let found = AtomicBool::new(false);
    let result = Mutex::new((0usize, 0usize));

    (0..=grid_h - pat_h).into_par_iter().for_each(|y| {
        if found.load(Ordering::Relaxed) {
            return;
        }

        for x in 0..=grid_w - pat_w {
            if found.load(Ordering::Relaxed) {
                break;
            }

            if pattern_matches(grid, grid_h, grid_w, pat, pat_h, pat_w, x, y) {
                let mut lock = result.lock().unwrap();
                *lock = (x, y);
                found.store(true, Ordering::Relaxed);
                break;
            }
        }
    });

    if found.load(Ordering::Relaxed) {
        let (x, y) = *result.lock().unwrap();
        unsafe {
            *out_x = x;
            *out_y = y;
        }
        true
    } else {
        false
    }
}

#[unsafe(no_mangle)]
pub extern "C" fn find_all_grid(
    grid_ptr: *const i64,
    grid_h: usize,
    grid_w: usize,
    pat_ptr: *const i64,
    pat_h: usize,
    pat_w: usize,
    out_ptr: *mut usize,
    max_out: usize,
) -> usize {
    let grid = unsafe { std::slice::from_raw_parts(grid_ptr, grid_h * grid_w) };
    let pat  = unsafe { std::slice::from_raw_parts(pat_ptr, pat_h * pat_w) };
    let out  = unsafe { std::slice::from_raw_parts_mut(out_ptr, max_out * 2) };

    if pat_h > grid_h || pat_w > grid_w {
        return 0;
    }

    // Collect matches in parallel
    let matches: Vec<(usize, usize)> = (0..=grid_h - pat_h).into_par_iter()
        .flat_map(|y| {
            let mut row_matches = Vec::new();
            for x in 0..=grid_w - pat_w {
                if pattern_matches(grid, grid_h, grid_w, pat, pat_h, pat_w, x, y) {
                    row_matches.push((x, y))
                }
            }
            row_matches
        })
        .collect();

    // Copy into out buffer (up to max_out)
    let mut count = 0;
    for &(x, y) in &matches {
        if count >= max_out { break; }
        out[count * 2] = x;
        out[count * 2 + 1] = y;
        count += 1;
    }

    count
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_find_grid_basic() {
        let grid: Vec<i64> = vec![
            1, 2, 3,
            4, 5, 6,
            7, 8, 9
        ];
        let pat: Vec<i64> = vec![
            5, 6,
            8, 9
        ];

        let mut out_x = 0usize;
        let mut out_y = 0usize;

        let found = find_grid(
            grid.as_ptr(),
            3, 3,
            pat.as_ptr(),
            2, 2,
            &mut out_x as *mut usize,
            &mut out_y as *mut usize
        );

        assert_eq!(found, true);
        assert_eq!(out_x, 1);
        assert_eq!(out_y, 1);
    }

    #[test]
    fn test_find_grid_not_found() {
        let grid: Vec<i64> = vec![1,2,3,4];
        let pat: Vec<i64> = vec![5];

        let mut out_x = 0usize;
        let mut out_y = 0usize;

        let found = find_grid(
            grid.as_ptr(),
            2, 2,
            pat.as_ptr(),
            1, 1,
            &mut out_x as *mut usize,
            &mut out_y as *mut usize
        );

        assert_eq!(found, false);
    }

    #[test]
    fn test_find_all_grid_basic() {
        let grid: Vec<i64> = vec![
            1, 2, 1,
            2, 1, 2,
            1, 2, 1
        ];
        let pat: Vec<i64> = vec![1, 2];

        let mut out_buf: Vec<usize> = vec![0; 10]; // enough space for 5 matches
        let count = find_all_grid(
            grid.as_ptr(),
            3, 3,
            pat.as_ptr(),
            1, 2,
            out_buf.as_mut_ptr(),
            5
        );

        assert_eq!(count, 3);
        assert_eq!(out_buf[..count*2], [0,0, 1,1, 0,2]);
    }
}
